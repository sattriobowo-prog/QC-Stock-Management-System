"""Server-side permission and role checks for QC Stock Management.

Only four roles are permitted across the system per Phase 1 governance:
QC Analyst, QC Admin, QC Manager, Admin.
"""

AVAILABLE_ROLES: list[str] = [
    "QC Analyst",
    "QC Admin",
    "QC Manager",
    "Admin",
]

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "QC Analyst": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "create_request",
        "issue_stock",
        "scan_lookup",
    ],
    "QC Admin": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "create_request",
        "issue_stock",
        "receive_stock",
        "create_adjustment",
        "manage_lots",
        "manage_documents",
        "manage_labels",
        "scan_lookup",
        "approve_transfer",
        "view_audit_log",
    ],
    "QC Manager": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "view_audit_log",
        "create_request",
        "approve_request",
        "issue_stock",
        "receive_stock",
        "create_adjustment",
        "approve_adjustment",
        "approve_transfer",
        "manage_vendors",
        "manage_documents",
        "release_lot",
        "scan_lookup",
    ],
    "Admin": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "view_audit_log",
        "create_request",
        "approve_request",
        "issue_stock",
        "receive_stock",
        "create_adjustment",
        "approve_adjustment",
        "approve_transfer",
        "manage_vendors",
        "manage_documents",
        "manage_labels",
        "manage_lots",
        "manage_users",
        "manage_settings",
        "release_lot",
        "migration_commit",
        "scan_lookup",
        "danger_zone",
    ],
}


def has_permission(role: str, permission: str) -> bool:
    """Server-side check: does the given role hold the given permission?"""
    return permission in ROLE_PERMISSIONS.get(role, [])


def require_permission(role: str, permission: str) -> tuple[bool, str]:
    """Return (allowed, reason). Use in service layer before mutating state."""
    if has_permission(role, permission):
        return (True, "")
    return (
        False,
        f"Role '{role}' is not authorized to perform '{permission}'.",
    )


def is_admin(role: str) -> bool:
    return role == "Admin"