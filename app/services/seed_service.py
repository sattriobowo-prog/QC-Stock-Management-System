"""Idempotent development seed helpers for the persistent data foundation.

These helpers are designed to be safe to invoke repeatedly: every seed
function checks for existing rows by their stable unique key (role name,
SKU, vendor code, location code, setting key, document-type name,
transaction-type code, FEFO reason code) and inserts only when missing.

GxP / CSV evidence notes (deferred to later phases):
  * Production seeding will run inside an Alembic migration / boot hook
    that wraps each seed in a transaction and emits an immutable audit
    entry per row. The helpers here are pure functions that return the
    rows that *would* be inserted, plus an in-memory upsert variant for
    the current Reflex state-driven app shell. No DDL is executed here.
  * Reflex-hosted DB integration is intentionally deferred — these
    helpers operate on plain dict sequences keyed by their unique
    identifier so they can be lifted directly into a SQLModel session
    when Phase 2 adds the persistence layer.
  * The seed set covers ONLY required reference data (roles, dev
    profile, default location, lookups, document types, FEFO reasons,
    transaction types, system settings). Transactional data
    (requests, issues, receivings, adjustments, transfers, audit log,
    notifications) is NEVER seeded — those rows must be created by
    user actions to preserve audit defensibility.
"""

from __future__ import annotations
from typing import Iterable
from datetime import datetime

from app.models.constants import (
    REQUIRED_ROLES,
    DOCUMENT_TYPES,
    FEFO_OVERRIDE_REASONS,
    TRANSACTION_TYPES,
    DEFAULT_MIGRATION_LOCATION_CODE,
    DEFAULT_MIGRATION_LOCATION_NAME,
    EXPIRY_WARNING_DAYS_DEFAULT,
    DEV_PROFILE_USER_ID,
    DEV_PROFILE_FULL_NAME,
    DEV_PROFILE_EMAIL,
    DEV_PROFILE_ROLE,
    LOT_STATUS_PENDING_RELEASE,
)
from app.services.permissions import ROLE_PERMISSIONS


# ---------------------------------------------------------------------------
# Generic idempotent upsert helper
# ---------------------------------------------------------------------------


def _upsert_by_key(
    rows: list[dict],
    candidates: Iterable[dict],
    key: str,
) -> tuple[int, int]:
    """Insert candidates into rows when the unique key is not present.

    Returns (inserted_count, skipped_count). Existing rows are never
    mutated — this preserves the idempotency contract.
    """
    existing = {r.get(key) for r in rows if key in r}
    inserted = 0
    skipped = 0
    for c in candidates:
        k = c.get(key)
        if k is None or k in existing:
            skipped += 1
            continue
        rows.append(dict(c))
        existing.add(k)
        inserted += 1
    return inserted, skipped


def _upsert_by_composite_key(
    rows: list[dict],
    candidates: Iterable[dict],
    key_cols: tuple[str, ...],
) -> tuple[int, int]:
    existing = {tuple(r.get(c) for c in key_cols) for r in rows}
    inserted = 0
    skipped = 0
    for c in candidates:
        k = tuple(c.get(col) for col in key_cols)
        if k in existing:
            skipped += 1
            continue
        rows.append(dict(c))
        existing.add(k)
        inserted += 1
    return inserted, skipped


# ---------------------------------------------------------------------------
# Seed payload builders (pure — no I/O)
# ---------------------------------------------------------------------------


def build_role_seed_rows() -> list[dict]:
    """Required four roles with their server-enforced permission sets."""
    return [
        {
            "name": role,
            "permissions": list(ROLE_PERMISSIONS.get(role, [])),
            "description": _role_description(role),
        }
        for role in REQUIRED_ROLES
    ]


def _role_description(role: str) -> str:
    return {
        "QC Analyst": (
            "Submits material requests and adjustment requests; can view "
            "released stock but cannot issue."
        ),
        "QC Admin": (
            "Reviews requests, issues approved stock, receives goods, "
            "uploads documents, performs expiry checks."
        ),
        "QC Manager": (
            "Approves adjustments, NAPZA requests, lot release/reject/"
            "quarantine, and master-data change requests."
        ),
        "Admin": (
            "Manages users, roles, settings, reference data, migration "
            "commit, and operational reset."
        ),
    }.get(role, "")


def build_dev_profile_seed_rows() -> list[dict]:
    """Single development profile — idempotent on user_id + email."""
    return [
        {
            "id": "PRF-DEV-0001",
            "user_id": DEV_PROFILE_USER_ID,
            "full_name": DEV_PROFILE_FULL_NAME,
            "email": DEV_PROFILE_EMAIL,
            "role": DEV_PROFILE_ROLE,
            "active": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    ]


def build_default_location_seed_rows() -> list[dict]:
    """The single mandatory default location: 'MIGRATION / UNASSIGNED'."""
    return [
        {
            "id": "LOC-MIG-0001",
            "code": DEFAULT_MIGRATION_LOCATION_CODE,
            "name": DEFAULT_MIGRATION_LOCATION_NAME,
            "description": (
                "Default landing zone for opening-balance migration AND "
                "the placeholder for items without a confirmed storage "
                "location. Per Phase 1 spec, this code is fixed."
            ),
            "restricted": False,
        }
    ]


def build_document_type_seed_rows() -> list[dict]:
    """Controlled-document categories — SDS, MSDS, COA, PO Evidence,
    Delivery Order, Other."""
    return [
        {
            "id": f"DC-{i + 1:03d}",
            "name": name,
            "description": _document_type_description(name),
            "retention_days": _document_type_retention(name),
            "required_for": _document_type_required_for(name),
        }
        for i, name in enumerate(DOCUMENT_TYPES)
    ]


def _document_type_description(name: str) -> str:
    return {
        "SDS": "Safety Data Sheet (current GHS format)",
        "MSDS": "Legacy Material Safety Data Sheet — retained for archival evidence",
        "COA": "Vendor Certificate of Analysis for a received lot",
        "PO Evidence": "Purchase order evidence record (vendor PO, quote, or order email)",
        "Delivery Order": "Delivery order or packing list accompanying a goods receipt",
        "Other": "Miscellaneous controlled document (catch-all)",
    }.get(name, "")


def _document_type_retention(name: str) -> int:
    return {
        "SDS": 3650,
        "MSDS": 3650,
        "COA": 1825,
        "PO Evidence": 2555,
        "Delivery Order": 2555,
        "Other": 1825,
    }.get(name, 1825)


def _document_type_required_for(name: str) -> str:
    return {
        "SDS": "Hazardous Items",
        "MSDS": "Hazardous Items (legacy)",
        "COA": "Receiving",
        "PO Evidence": "Receiving",
        "Delivery Order": "Receiving",
        "Other": "Optional",
    }.get(name, "Optional")


def build_fefo_override_reason_seed_rows() -> list[dict]:
    """Structured FEFO override reason codes."""
    return [
        {
            "code": code,
            "label": _fefo_reason_label(code),
            "description": _fefo_reason_description(code),
        }
        for code in FEFO_OVERRIDE_REASONS
    ]


def _fefo_reason_label(code: str) -> str:
    return {
        "Operational need": "Operational need",
        "QC hold avoidance": "QC hold avoidance",
        "Container already open": "Container already open",
        "Location access constraint": "Location access constraint",
        "Other": "Other (free-text comment required)",
    }.get(code, code)


def _fefo_reason_description(code: str) -> str:
    return {
        "Operational need": (
            "Immediate analytical or operational requirement to use this specific lot."
        ),
        "QC hold avoidance": (
            "Bypassing a lot currently under QC investigation or administrative hold."
        ),
        "Container already open": (
            "Using an already opened container to minimize waste and contamination risk."
        ),
        "Location access constraint": (
            "Earliest-expiry lot is physically inaccessible due to storage or safety constraints."
        ),
        "Other": (
            "Catch-all reason — a free-text comment is mandatory and is "
            "captured on FefoOverride.comment for audit defensibility."
        ),
    }.get(code, "")


def build_transaction_type_seed_rows() -> list[dict]:
    """Stock-ledger transaction-type enum rows."""
    return [
        {
            "code": code,
            "label": _transaction_type_label(code),
            "direction": _transaction_type_direction(code),
            "description": _transaction_type_description(code),
        }
        for code in TRANSACTION_TYPES
    ]


def _transaction_type_label(code: str) -> str:
    return {
        "opening_balance": "Opening Balance",
        "receive": "Receive",
        "issue": "Issue / Consume",
        "transfer": "Internal Transfer",
        "adjust": "Adjustment",
        "dispose": "Disposal",
        "quarantine": "Quarantine",
        "release": "Release",
        "reject": "Reject",
        "reservation": "Reservation",
    }.get(code, code)


def _transaction_type_direction(code: str) -> str:
    return {
        "opening_balance": "+",
        "receive": "+",
        "issue": "-",
        "transfer": "0",
        "adjust": "+/-",
        "dispose": "-",
        "quarantine": "0",
        "release": "0",
        "reject": "0",
        "reservation": "0",
    }.get(code, "0")


def _transaction_type_description(code: str) -> str:
    return {
        "opening_balance": "Migration credit posted as Released opening balance",
        "receive": "Goods receipt — defaults to Pending Release",
        "issue": "FEFO-driven consumption against a Released lot",
        "transfer": "Move stock between locations (no net change)",
        "adjust": "Approved positive or negative correction",
        "dispose": "Expired or quarantined lot disposal",
        "quarantine": "Lot status change to Quarantine — blocks issue",
        "release": "QC release moves a lot into available stock",
        "reject": "QC reject — lot blocked from issue, retained for evidence",
        "reservation": "Soft hold on stock for an approved request",
    }.get(code, "")


def build_system_setting_seed_rows() -> list[dict]:
    """Default system-setting rows including expiry_warning_days=90."""
    return [
        {
            "key": "expiry_warning_days",
            "label": "Expiry warning days",
            "value": str(EXPIRY_WARNING_DAYS_DEFAULT),
            "category": "Notifications",
            "description": (
                "Lot is flagged as expiring soon when days-to-expiry ≤ "
                "this value (Phase 1 default = 90)."
            ),
        },
        {
            "key": "fefo_strict",
            "label": "Strict FEFO enforcement",
            "value": "On",
            "category": "Inventory",
            "description": (
                "Issue must use earliest-expiry lot unless override "
                "reason and comment are provided."
            ),
        },
        {
            "key": "negative_stock",
            "label": "Allow negative stock",
            "value": "Off",
            "category": "Inventory",
            "description": (
                "Service layer rejects any operation that would result "
                "in negative on-hand."
            ),
        },
        {
            "key": "self_approval",
            "label": "Allow self-approval",
            "value": "Off",
            "category": "Governance",
            "description": (
                "Submitter cannot approve their own request or adjustment."
            ),
        },
        {
            "key": "default_release_status",
            "label": "Default lot status on receiving",
            "value": LOT_STATUS_PENDING_RELEASE,
            "category": "Receiving",
            "description": (
                "Newly received lots require QC release before becoming "
                "available."
            ),
        },
        {
            "key": "napza_dual_signoff",
            "label": "NAPZA dual sign-off",
            "value": "Required",
            "category": "Governance",
            "description": (
                "NAPZA issue and adjustment require two approvals."
            ),
        },
        {
            "key": "audit_immutability",
            "label": "Audit ledger immutability",
            "value": "Enforced",
            "category": "Governance",
            "description": (
                "Audit log entries are append-only — never edited or deleted."
            ),
        },
        {
            "key": "migration_lot_tag",
            "label": "Migration lot tag",
            "value": "MIG",
            "category": "Migration",
            "description": (
                "Opening balances import lots with the MIG- prefix."
            ),
        },
        {
            "key": "migration_holding_location",
            "label": "Migration holding location",
            "value": DEFAULT_MIGRATION_LOCATION_CODE,
            "category": "Migration",
            "description": (
                "Default location code for migrated opening-balance lots."
            ),
        },
    ]


# ---------------------------------------------------------------------------
# Idempotent in-memory seed orchestrator
# ---------------------------------------------------------------------------


def seed_all(
    *,
    roles: list[dict] | None = None,
    profiles: list[dict] | None = None,
    locations: list[dict] | None = None,
    document_types: list[dict] | None = None,
    fefo_reasons: list[dict] | None = None,
    transaction_types: list[dict] | None = None,
    system_settings: list[dict] | None = None,
) -> dict[str, tuple[int, int]]:
    """Idempotently apply every Phase 1 reference seed to the supplied
    in-memory collections. Each kwarg is a list that will be mutated in
    place — pass [] to start from scratch, or pass an existing seeded
    list to top-up missing rows without disturbing user edits.

    Returns a per-domain (inserted, skipped) summary suitable for logging
    or surfacing in a developer-only diagnostics page.
    """
    summary: dict[str, tuple[int, int]] = {}

    if roles is not None:
        summary["roles"] = _upsert_by_key(roles, build_role_seed_rows(), "name")
    if profiles is not None:
        summary["profiles"] = _upsert_by_key(
            profiles, build_dev_profile_seed_rows(), "user_id"
        )
    if locations is not None:
        summary["locations"] = _upsert_by_key(
            locations, build_default_location_seed_rows(), "code"
        )
    if document_types is not None:
        summary["document_types"] = _upsert_by_key(
            document_types, build_document_type_seed_rows(), "name"
        )
    if fefo_reasons is not None:
        summary["fefo_reasons"] = _upsert_by_key(
            fefo_reasons, build_fefo_override_reason_seed_rows(), "code"
        )
    if transaction_types is not None:
        summary["transaction_types"] = _upsert_by_key(
            transaction_types, build_transaction_type_seed_rows(), "code"
        )
    if system_settings is not None:
        summary["system_settings"] = _upsert_by_key(
            system_settings, build_system_setting_seed_rows(), "key"
        )

    return summary


__all__ = [
    "build_role_seed_rows",
    "build_dev_profile_seed_rows",
    "build_default_location_seed_rows",
    "build_document_type_seed_rows",
    "build_fefo_override_reason_seed_rows",
    "build_transaction_type_seed_rows",
    "build_system_setting_seed_rows",
    "seed_all",
]