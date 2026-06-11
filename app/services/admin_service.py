"""Admin-only governance helpers — operational reset preserves accounts/roles.

GxP / CSV evidence collection points:
  * `build_operational_reset_plan` returns the exact set of operational
    tables to truncate AND the protected reference/account tables that
    MUST be preserved. Persistence layer wraps the truncations in one
    transaction with an OPERATIONAL_RESET audit entry.
  * Reset is Admin-only AND requires the literal token 'RESET' as a
    second-factor confirmation. Both checks are server-side.
"""

from __future__ import annotations
from datetime import datetime
from app.services.permissions import has_permission
from app.services.audit_service import build_audit_entry


RESET_CONFIRM_TOKEN = "RESET"

# Reference / account tables — never wiped.
PRESERVED_DOMAINS: tuple[str, ...] = (
    "users",
    "roles",
    "accounts",
    "permissions",
    "profiles",
    "system_settings",
    "vendors",
    "items",
    "lots_master",
    "categories",
    "forms",
    "storage_conditions",
    "toxicity_classes",
    "napza_classes",
    "locations",
    "document_categories",
    "fefo_override_reasons",
    "transaction_types",
)

# Operational tables — wiped on reset.
CLEARED_DOMAINS: tuple[str, ...] = (
    "material_requests",
    "material_request_lines",
    "reservations",
    "issues",
    "fefo_overrides",
    "receivings",
    "lot_receipts",
    "adjustments",
    "pending_adjustments",
    "transfers",
    "expiry_check_tasks",
    "notifications",
    "audit_log",
    "stock_transactions",
    "stock_balances",
    "lots",
    "documents",
    "master_data_change_requests",
    "migration_batches",
    "migration_import_rows",
    "purchase_orders",
    "purchase_order_lines",
)


def can_perform_reset(role: str, confirm_text: str) -> tuple[bool, str]:
    if not has_permission(role, "danger_zone"):
        return (
            False,
            f"Role '{role}' is not authorized for Danger Zone actions.",
        )
    if confirm_text.strip() != RESET_CONFIRM_TOKEN:
        return (
            False,
            f"Confirmation token must equal '{RESET_CONFIRM_TOKEN}'.",
        )
    return (True, "OK")


def can_commit_migration(role: str) -> tuple[bool, str]:
    if not has_permission(role, "migration_commit"):
        return (
            False,
            f"Role '{role}' is not authorized to commit migration batches.",
        )
    return (True, "OK")


def build_operational_reset_plan(
    role: str,
    confirm_text: str,
    user: str,
) -> tuple[bool, str, dict]:
    """Pure plan builder for an Admin operational reset.

    Returns (ok, reason, plan) with:
        plan["preserve"] — tables that MUST NOT be touched
        plan["clear"]    — operational tables to truncate
        plan["audit"]    — AuditLog entry to write after truncation
        plan["confirm_token"] — the token actually supplied
        plan["timestamp"] — UTC-naive timestamp
    The caller is responsible for executing the truncation inside a
    single `async with rx.asession()` transaction (raw SQL TRUNCATE or
    DELETE per the PG dialect) and then inserting the audit entry.
    """
    ok, reason = can_perform_reset(role, confirm_text)
    if not ok:
        return (False, reason, {})

    audit = build_audit_entry(
        user=user,
        role=role,
        action="OPERATIONAL_RESET",
        target="system",
        detail=(
            "Operational reset: cleared "
            f"{len(CLEARED_DOMAINS)} operational tables; preserved "
            f"{len(PRESERVED_DOMAINS)} reference/account tables."
        ),
    )
    return (
        True,
        "OK",
        {
            "preserve": list(PRESERVED_DOMAINS),
            "clear": list(CLEARED_DOMAINS),
            "audit": audit,
            "confirm_token": confirm_text.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )