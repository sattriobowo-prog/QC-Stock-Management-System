import reflex as rx
from app.services.permissions import ROLE_PERMISSIONS, AVAILABLE_ROLES


# Phase 1 note: the in-app role switcher (set_role) is a LOCAL DEVELOPMENT
# convenience only. In production the active role will be derived from the
# authenticated user's UserProfile and cannot be changed at runtime by the
# user. The corresponding UI surfaces are clearly labeled as dev-only.
DEMO_ROLE_SWITCHER_ENABLED = True


class AuthState(rx.State):
    current_user: str = "Dr. Sarah Chen"
    current_role: str = "QC Manager"
    available_roles: list[str] = AVAILABLE_ROLES
    role_permissions: dict[str, list[str]] = ROLE_PERMISSIONS
    demo_mode: bool = DEMO_ROLE_SWITCHER_ENABLED

    @rx.var
    def current_permissions(self) -> list[str]:
        return self.role_permissions.get(self.current_role, [])

    @rx.event
    def set_role(self, role: str):
        if not self.demo_mode:
            yield rx.toast.error(
                "Role switching is disabled outside local development."
            )
            return
        self.current_role = role
        yield rx.toast(f"[Dev] Switched to role: {role}", duration=2000)