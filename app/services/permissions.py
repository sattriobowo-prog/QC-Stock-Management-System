"""Server-side permission and role checks for QC Stock Management.

Only four roles are permitted across the system per Phase 1 governance:
QC Analyst, QC Admin, QC Manager, Admin.

Permission matrix (server-enforced):

  * QC Analyst — view inventory / released stock, submit material requests,
    view own requests, submit adjustment requests only.
    EXPLICITLY DOES NOT have `issue_stock`.

  * QC Admin — review requests, issue after approval, receive stock,
    upload documents, perform expiry checks, submit adjustments,
    propose master data changes.

  * QC Manager — approve/reject adjustments, NAPZA requests, lot release/
    reject/quarantine, master data changes; reports/dashboards/audit.

  * Admin — manage users/roles/settings/reference data, import migration
    CSV, reset operational data.
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
        "view_released_stock",
        "create_request",
        "view_own_requests",
        "submit_adjustment_request",
        "scan_lookup",
    ],
    "QC Admin": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "view_audit_log",
        "view_released_stock",
        "create_request",
        "review_request",
        "issue_stock",
        "receive_stock",
        "create_adjustment",
        "submit_adjustment_request",
        "manage_lots",
        "manage_documents",
        "upload_documents",
        "manage_labels",
        "perform_expiry_check",
        "propose_master_data_change",
        "scan_lookup",
    ],
    "QC Manager": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "view_audit_log",
        "view_released_stock",
        "approve_request",
        "approve_napza_request",
        "approve_adjustment",
        "approve_transfer",
        "release_lot",
        "reject_lot",
        "quarantine_lot",
        "approve_master_data_change",
        "manage_vendors",
        "manage_documents",
        "scan_lookup",
    ],
    "Admin": [
        "view_inventory",
        "view_lots",
        "view_documents",
        "view_reports",
        "view_audit_log",
        "view_released_stock",
        "manage_users",
        "manage_roles",
        "manage_settings",
        "manage_reference_data",
        "manage_vendors",
        "manage_documents",
        "manage_labels",
        "manage_lots",
        "release_lot",
        "reject_lot",
        "quarantine_lot",
        "migration_commit",
        "scan_lookup",
        "danger_zone",
        "operational_reset",
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