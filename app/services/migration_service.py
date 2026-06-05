"""Opening-balance migration helpers.

Migrated lots are tagged with the MIG prefix, placed in the Migration
Holding Area (or UNASSIGNED when unknown), and posted as Released
opening-balance transactions. Returned payloads are PostgreSQL-compatible
and include durable fields (`expiry_known`, nullable `expiry_date`,
`qc_status`, `status`) aligned with the persistent foundation.
"""

from __future__ import annotations
from datetime import datetime, date
import uuid
import logging

MIGRATION_LOT_PREFIX = "MIG"
MIGRATION_LOCATION = "Migration Holding Area"
DEFAULT_UNASSIGNED_LOCATION = "UNASSIGNED"
MIGRATION_STATUS = "Released"
MIGRATION_QC_STATUS = "Released"
MIGRATION_VENDOR = "Migration"

UNKNOWN_EXPIRY_TOKENS = {"", "—", "-", "None", "none", "null", "NULL"}


def normalize_migration_lot(raw_lot: str, sku: str, row_no: int) -> str:
    """Ensure the lot number carries the MIG prefix."""
    raw_lot = (raw_lot or "").strip()
    if not raw_lot:
        safe_sku = (sku or "ITEM").strip() or "ITEM"
        return f"{MIGRATION_LOT_PREFIX}-{safe_sku}-{row_no:03d}"
    if raw_lot.startswith(f"{MIGRATION_LOT_PREFIX}-"):
        return raw_lot
    return f"{MIGRATION_LOT_PREFIX}-{raw_lot}"


def is_known_expiry(expiry_iso: str | None) -> bool:
    if expiry_iso is None:
        return False
    if expiry_iso.strip() in UNKNOWN_EXPIRY_TOKENS:
        return False
    try:
        yyyy, mm, dd = expiry_iso.strip().split("-")
        date(int(yyyy), int(mm), int(dd))
        return True
    except Exception:
        logging.exception("Unexpected error")
        return False


def days_to_expiry(expiry_iso: str | None, today: date | None = None) -> int:
    """Compute days-to-expiry. Unknown / blank → very large sentinel.

    Using a sentinel (10**9) rather than a fabricated 365 days keeps
    unknown-expiry lots from sorting ahead of dated lots in FEFO.
    """
    if not is_known_expiry(expiry_iso):
        return 10**9
    today = today or date.today()
    try:
        yyyy, mm, dd = expiry_iso.strip().split("-")
        return (date(int(yyyy), int(mm), int(dd)) - today).days
    except Exception:
        logging.exception("Failed to compute days-to-expiry")
        return 10**9


def normalize_location(location: str | None) -> str:
    """Empty / unknown location falls back to MIGRATION holding; explicit
    'UNASSIGNED' is preserved verbatim."""
    loc = (location or "").strip()
    if not loc:
        return MIGRATION_LOCATION
    return loc


def build_opening_balance_lot(
    item_id: str,
    item_name: str,
    sku: str,
    quantity: float,
    unit: str,
    expiry: str | None,
    location: str | None,
    raw_lot: str,
    row_no: int,
) -> dict:
    """Construct a Released opening-balance lot for migration.

    Returned dict is PostgreSQL-compatible and includes durable fields
    used by the persistent foundation tests:
        - expiry_known (bool)
        - expiry_date (str | None) — nullable when unknown
        - qc_status / status (both 'Released' for migration)
        - lot_number with MIG- prefix
        - location defaulting to MIGRATION holding (or UNASSIGNED)
    """
    if quantity < 0:
        raise ValueError(
            "Negative opening balances are not permitted (service-layer rule)."
        )

    expiry_clean = expiry.strip() if isinstance(expiry, str) else expiry
    expiry_known = is_known_expiry(expiry_clean)
    expiry_date_value: str | None = expiry_clean if expiry_known else None

    return {
        "id": f"LOT-{uuid.uuid4().hex[:6].upper()}",
        "item_id": item_id,
        "item_name": item_name,
        "sku": sku,
        "lot_number": normalize_migration_lot(raw_lot, sku, row_no),
        "quantity": float(quantity),
        "unit": unit,
        "received_date": datetime.now().strftime("%Y-%m-%d"),
        "expiry_date": expiry_date_value,
        "expiry_known": expiry_known,
        "status": MIGRATION_STATUS,
        "qc_status": MIGRATION_QC_STATUS,
        "location": normalize_location(location),
        "vendor": MIGRATION_VENDOR,
        "days_to_expiry": days_to_expiry(expiry_clean),
        "is_migration": True,
        "migration_batch": None,
    }