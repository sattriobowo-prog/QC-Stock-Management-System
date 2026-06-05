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
MIGRATION_LOCATION = "MIGRATION / UNASSIGNED"
DEFAULT_UNASSIGNED_LOCATION = "MIGRATION / UNASSIGNED"
MIGRATION_STATUS = "Released"
MIGRATION_QC_STATUS = "released"
MIGRATION_VENDOR = "Migration"
MIGRATION_TRANSACTION_TYPE = "opening_balance"

UNKNOWN_EXPIRY_TOKENS = {"", "—", "-", "None", "none", "null", "NULL"}


def normalize_migration_lot(raw_lot: str, sku: str, row_no: int = 0) -> str:
    """Per spec: opening-balance lot_number is exactly `MIG-<sku>`.

    The raw_lot column is ignored to enforce a single deterministic lot
    per SKU at migration time. row_no is accepted for backwards
    compatibility but unused — preserved for callers passing it.
    """
    safe_sku = (sku or "ITEM").strip() or "ITEM"
    return f"{MIGRATION_LOT_PREFIX}-{safe_sku}"


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
    """Compute days-to-expiry. Unknown / blank → sentinel 10**9."""
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
    """Empty/unknown location falls back to 'MIGRATION / UNASSIGNED'; explicit
    'UNASSIGNED' is normalized to 'MIGRATION / UNASSIGNED' per requirement."""
    loc = (location or "").strip()
    if not loc:
        return MIGRATION_LOCATION
    if loc.upper() in (
        "MIGRATION",
        "UNASSIGNED",
        "MIGRATION / UNASSIGNED",
        "MIGRATION HOLDING AREA",
    ):
        return "MIGRATION / UNASSIGNED"
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
    # Per spec: when expiry is unknown, expiry_date MUST be None — never
    # the legacy fake placeholder '2099-12-31'.
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
        "transaction_type": MIGRATION_TRANSACTION_TYPE,
    }


def build_opening_balance_transaction(
    item_id: str,
    lot_number: str,
    quantity: float,
    unit: str,
    location: str,
    user: str,
    role: str,
    batch_no: str = "",
) -> dict:
    """Immutable StockTransaction payload for an opening-balance import.

    The transaction_type is exactly 'opening_balance' (lower-snake) per
    Phase 1 spec. Caller persists this verbatim alongside an AuditLog
    entry built via app.services.audit_service.build_audit_entry.
    """
    return {
        "id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_type": MIGRATION_TRANSACTION_TYPE,
        "item_id": item_id,
        "lot_number": lot_number,
        "location": normalize_location(location),
        "delta": float(quantity),
        "unit": unit,
        "user": user,
        "role": role,
        "reference": batch_no,
        "notes": "Opening balance — migrated from legacy system",
    }


def build_or_update_stock_balance(
    existing_balances: list[dict],
    item_id: str,
    lot_number: str,
    location: str,
    quantity: float,
    unit: str,
) -> tuple[dict, bool]:
    """Idempotent StockBalance upsert helper.

    Returns (balance, created) where `created=True` iff a new balance row
    was inserted into existing_balances. The unique key is
    (item_id, lot_number, location). Caller is responsible for persisting.
    """
    loc = normalize_location(location)
    for b in existing_balances:
        if (
            b.get("item_id") == item_id
            and b.get("lot_number") == lot_number
            and b.get("location") == loc
        ):
            b["quantity"] = round(
                float(b.get("quantity", 0)) + float(quantity), 4
            )
            return (b, False)
    new_balance = {
        "id": f"BAL-{uuid.uuid4().hex[:6].upper()}",
        "item_id": item_id,
        "lot_number": lot_number,
        "location": loc,
        "quantity": round(float(quantity), 4),
        "unit": unit,
    }
    existing_balances.append(new_balance)
    return (new_balance, True)