import reflex as rx


class AuthState(rx.State):
    current_user: str = "Dr. Sarah Chen"
    current_role: str = "QC Manager"
    available_roles: list[str] = [
        "QC Manager",
        "QC Analyst",
        "Warehouse Officer",
        "Approver",
        "Auditor",
        "Admin",
    ]
    role_permissions: dict[str, list[str]] = {
        "QC Manager": [
            "view_inventory",
            "create_request",
            "approve_request",
            "issue_stock",
            "receive_stock",
            "create_adjustment",
            "approve_adjustment",
            "manage_vendors",
            "view_reports",
        ],
        "QC Analyst": [
            "view_inventory",
            "create_request",
            "issue_stock",
            "view_reports",
        ],
        "Warehouse Officer": [
            "view_inventory",
            "receive_stock",
            "issue_stock",
            "create_adjustment",
            "manage_lots",
            "view_reports",
        ],
        "Approver": [
            "view_inventory",
            "approve_request",
            "approve_adjustment",
            "view_reports",
        ],
        "Auditor": [
            "view_inventory",
            "view_reports",
            "view_audit_log",
        ],
        "Admin": [
            "view_inventory",
            "create_request",
            "approve_request",
            "issue_stock",
            "receive_stock",
            "create_adjustment",
            "approve_adjustment",
            "manage_vendors",
            "manage_users",
            "manage_settings",
            "view_reports",
            "view_audit_log",
            "danger_zone",
        ],
    }

    @rx.var
    def current_permissions(self) -> list[str]:
        return self.role_permissions.get(self.current_role, [])

    @rx.event
    def set_role(self, role: str):
        self.current_role = role
        yield rx.toast(f"Switched to role: {role}", duration=2000)