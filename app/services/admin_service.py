"""Admin-only governance helpers — operational reset preserves accounts/roles."""

from __future__ import annotations
from app.services.permissions import has_permission


RESET_CONFIRM_TOKEN = "RESET"

PRESERVED_DOMAINS = (
    "users",
    "roles",
    "accounts",
    "permissions",
    "system_settings",
    "vendors",
    "items",
    "lots_master",
    "document_categories",
)

CLEARED_DOMAINS = (
    "material_requests",
    "issues",
    "receivings",
    "adjustments",
    "transfers",
    "expiry_tasks",
    "notifications",
    "audit_log",
    "stock_transactions",
    "migration_pending",
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