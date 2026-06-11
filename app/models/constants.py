"""Phase 1 persistent-foundation constants.

These constants define the canonical enumerations referenced across the
persistent data foundation. They are intentionally framework-light so
they can be reused by the seed helpers and by a future ORM mapping
layer without churn.

GxP / CSV evidence collection points (deferred to later phases):
  * Every value in TRANSACTION_TYPES is an append-only stock-ledger
    event class. The ledger is the system of record for product flow
    and must remain immutable for GxP audit defensibility.
  * Every value in DOCUMENT_TYPES corresponds to a controlled-document
    category whose retention/expiry rules are configured in
    DocumentCategory and enforced by service-layer validation.
  * Every value in FEFO_OVERRIDE_REASONS is a structured reason code
    captured on the FefoOverride entity to provide GxP-grade evidence
    when an analyst bypasses the earliest-expiry lot.
  * EXPIRY_WARNING_DAYS_DEFAULT seeds the system setting that drives
    expiry-soon notifications and the Expiry Check Task generator.
"""

from __future__ import annotations
from typing import Final


# ---------------------------------------------------------------------------
# Roles (Phase 1 — exactly four roles; see app.services.permissions)
# ---------------------------------------------------------------------------

REQUIRED_ROLES: Final[tuple[str, ...]] = (
    "QC Analyst",
    "QC Admin",
    "QC Manager",
    "Admin",
)


# ---------------------------------------------------------------------------
# Stock-ledger transaction types (append-only)
# ---------------------------------------------------------------------------
# These values are the canonical `transaction_type` enum on the
# StockTransaction entity. The ledger is append-only — a transaction is
# never edited or deleted; corrections are posted as compensating rows.

TRANSACTION_TYPE_OPENING_BALANCE: Final[str] = "opening_balance"
TRANSACTION_TYPE_RECEIVE: Final[str] = "receive"
TRANSACTION_TYPE_ISSUE: Final[str] = "issue"
TRANSACTION_TYPE_TRANSFER: Final[str] = "transfer"
TRANSACTION_TYPE_ADJUST: Final[str] = "adjust"
TRANSACTION_TYPE_DISPOSE: Final[str] = "dispose"
TRANSACTION_TYPE_QUARANTINE: Final[str] = "quarantine"
TRANSACTION_TYPE_RELEASE: Final[str] = "release"
TRANSACTION_TYPE_REJECT: Final[str] = "reject"
TRANSACTION_TYPE_RESERVATION: Final[str] = "reservation"

TRANSACTION_TYPES: Final[tuple[str, ...]] = (
    TRANSACTION_TYPE_OPENING_BALANCE,
    TRANSACTION_TYPE_RECEIVE,
    TRANSACTION_TYPE_ISSUE,
    TRANSACTION_TYPE_TRANSFER,
    TRANSACTION_TYPE_ADJUST,
    TRANSACTION_TYPE_DISPOSE,
    TRANSACTION_TYPE_QUARANTINE,
    TRANSACTION_TYPE_RELEASE,
    TRANSACTION_TYPE_REJECT,
    TRANSACTION_TYPE_RESERVATION,
)


# ---------------------------------------------------------------------------
# Document types (controlled-document categories)
# ---------------------------------------------------------------------------
# Used by Document.category and DocumentCategory.name. Retention windows
# are configured per-category by the Admin role; the values below are
# the canonical seed list.

DOCUMENT_TYPE_SDS: Final[str] = "SDS"
DOCUMENT_TYPE_MSDS: Final[str] = "MSDS"
DOCUMENT_TYPE_COA: Final[str] = "COA"
DOCUMENT_TYPE_PO_EVIDENCE: Final[str] = "PO Evidence"
DOCUMENT_TYPE_DELIVERY_ORDER: Final[str] = "Delivery Order"
DOCUMENT_TYPE_OTHER: Final[str] = "Other"

DOCUMENT_TYPES: Final[tuple[str, ...]] = (
    DOCUMENT_TYPE_SDS,
    DOCUMENT_TYPE_MSDS,
    DOCUMENT_TYPE_COA,
    DOCUMENT_TYPE_PO_EVIDENCE,
    DOCUMENT_TYPE_DELIVERY_ORDER,
    DOCUMENT_TYPE_OTHER,
)


# -------------------------------------------------------------------------
# FEFO override reason codes
# -------------------------------------------------------------------------
# Captured on FefoOverride.reason when an analyst bypasses the
# earliest-expiry lot. A free-text comment is also required for GxP
# audit defensibility (captured separately on FefoOverride.comment).

FEFO_REASON_OPERATIONAL_NEED: Final[str] = "Operational need"
FEFO_REASON_QC_HOLD_AVOIDANCE: Final[str] = "QC hold avoidance"
FEFO_REASON_CONTAINER_ALREADY_OPEN: Final[str] = "Container already open"
FEFO_REASON_LOCATION_ACCESS_CONSTRAINT: Final[str] = (
    "Location access constraint"
)
FEFO_REASON_OTHER: Final[str] = "Other"

FEFO_OVERRIDE_REASONS: Final[tuple[str, ...]] = (
    FEFO_REASON_OPERATIONAL_NEED,
    FEFO_REASON_QC_HOLD_AVOIDANCE,
    FEFO_REASON_CONTAINER_ALREADY_OPEN,
    FEFO_REASON_LOCATION_ACCESS_CONSTRAINT,
    FEFO_REASON_OTHER,
)


# ---------------------------------------------------------------------------
# Lot QC status values
# ---------------------------------------------------------------------------

LOT_STATUS_PENDING_RELEASE: Final[str] = "Pending Release"
LOT_STATUS_RELEASED: Final[str] = "Released"
LOT_STATUS_QUARANTINE: Final[str] = "Quarantine"
LOT_STATUS_REJECTED: Final[str] = "Rejected"
LOT_STATUS_EXPIRED: Final[str] = "Expired"

LOT_STATUSES: Final[tuple[str, ...]] = (
    LOT_STATUS_PENDING_RELEASE,
    LOT_STATUS_RELEASED,
    LOT_STATUS_QUARANTINE,
    LOT_STATUS_REJECTED,
    LOT_STATUS_EXPIRED,
)


# ---------------------------------------------------------------------------
# Default migration / unassigned location code
# ---------------------------------------------------------------------------
# Phase 1 spec mandates the default landing zone for opening-balance
# migration AND the placeholder for items without a confirmed home is
# EXACTLY the string below.

DEFAULT_MIGRATION_LOCATION_CODE: Final[str] = "MIGRATION / UNASSIGNED"
DEFAULT_MIGRATION_LOCATION_NAME: Final[str] = "MIGRATION / UNASSIGNED"


# ---------------------------------------------------------------------------
# System setting defaults
# ---------------------------------------------------------------------------

EXPIRY_WARNING_DAYS_DEFAULT: Final[int] = 90
NEGATIVE_STOCK_ALLOWED_DEFAULT: Final[bool] = False
SELF_APPROVAL_ALLOWED_DEFAULT: Final[bool] = False
FEFO_STRICT_DEFAULT: Final[bool] = True
NAPZA_DUAL_SIGNOFF_DEFAULT: Final[bool] = True
DEFAULT_RECEIVING_STATUS: Final[str] = LOT_STATUS_PENDING_RELEASE
MIGRATION_LOT_PREFIX_DEFAULT: Final[str] = "MIG"
AUDIT_IMMUTABLE_DEFAULT: Final[bool] = True


# ---------------------------------------------------------------------------
# Dev profile (idempotent seed target — see app.services.seed_service)
# ---------------------------------------------------------------------------

DEV_PROFILE_USER_ID: Final[str] = "USR-DEV-0001"
DEV_PROFILE_FULL_NAME: Final[str] = "Dr. Sarah Chen"
DEV_PROFILE_EMAIL: Final[str] = "sarah.chen@qclab.local"
DEV_PROFILE_ROLE: Final[str] = "QC Manager"


__all__ = [
    "REQUIRED_ROLES",
    "TRANSACTION_TYPES",
    "TRANSACTION_TYPE_OPENING_BALANCE",
    "TRANSACTION_TYPE_RECEIVE",
    "TRANSACTION_TYPE_ISSUE",
    "TRANSACTION_TYPE_TRANSFER",
    "TRANSACTION_TYPE_ADJUST",
    "TRANSACTION_TYPE_DISPOSE",
    "TRANSACTION_TYPE_QUARANTINE",
    "TRANSACTION_TYPE_RELEASE",
    "TRANSACTION_TYPE_REJECT",
    "TRANSACTION_TYPE_RESERVATION",
    "DOCUMENT_TYPES",
    "DOCUMENT_TYPE_SDS",
    "DOCUMENT_TYPE_MSDS",
    "DOCUMENT_TYPE_COA",
    "DOCUMENT_TYPE_PO_EVIDENCE",
    "DOCUMENT_TYPE_DELIVERY_ORDER",
    "DOCUMENT_TYPE_OTHER",
    "FEFO_OVERRIDE_REASONS",
    "FEFO_REASON_OPERATIONAL_NEED",
    "FEFO_REASON_QC_HOLD_AVOIDANCE",
    "FEFO_REASON_CONTAINER_ALREADY_OPEN",
    "FEFO_REASON_LOCATION_ACCESS_CONSTRAINT",
    "FEFO_REASON_OTHER",
    "LOT_STATUSES",
    "LOT_STATUS_PENDING_RELEASE",
    "LOT_STATUS_RELEASED",
    "LOT_STATUS_QUARANTINE",
    "LOT_STATUS_REJECTED",
    "LOT_STATUS_EXPIRED",
    "DEFAULT_MIGRATION_LOCATION_CODE",
    "DEFAULT_MIGRATION_LOCATION_NAME",
    "EXPIRY_WARNING_DAYS_DEFAULT",
    "NEGATIVE_STOCK_ALLOWED_DEFAULT",
    "SELF_APPROVAL_ALLOWED_DEFAULT",
    "FEFO_STRICT_DEFAULT",
    "NAPZA_DUAL_SIGNOFF_DEFAULT",
    "DEFAULT_RECEIVING_STATUS",
    "MIGRATION_LOT_PREFIX_DEFAULT",
    "AUDIT_IMMUTABLE_DEFAULT",
    "DEV_PROFILE_USER_ID",
    "DEV_PROFILE_FULL_NAME",
    "DEV_PROFILE_EMAIL",
    "DEV_PROFILE_ROLE",
]