import reflex as rx
from app.services.permissions import ROLE_PERMISSIONS, AVAILABLE_ROLES


class AuthState(rx.State):
    current_user: str = "Dr. Sarah Chen"
    current_role: str = "QC Manager"
    available_roles: list[str] = AVAILABLE_ROLES
    role_permissions: dict[str, list[str]] = ROLE_PERMISSIONS

    @rx.var
    def current_permissions(self) -> list[str]:
        return self.role_permissions.get(self.current_role, [])

    @rx.event
    def set_role(self, role: str):
        self.current_role = role
        yield rx.toast(f"Switched to role: {role}", duration=2000)