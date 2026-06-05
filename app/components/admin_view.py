import reflex as rx
from app.states.auth_state import AuthState


def role_card(role: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("shield-check", class_name="h-4 w-4 text-blue-600"),
                rx.el.span(
                    role, class_name="text-sm font-semibold text-gray-900"
                ),
                class_name="flex items-center gap-2",
            ),
            rx.cond(
                AuthState.current_role == role,
                rx.el.span(
                    "Active",
                    class_name="text-[10px] font-semibold px-2 py-0.5 rounded bg-green-50 text-green-700 border border-green-200",
                ),
                rx.el.button(
                    "Switch",
                    on_click=lambda: AuthState.set_role(role),
                    class_name="text-xs font-medium text-blue-600 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50",
                ),
            ),
            class_name="flex items-center justify-between mb-3",
        ),
        rx.el.div(
            rx.el.div(
                "Permissions",
                class_name="text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    AuthState.role_permissions[role],
                    lambda perm: rx.el.span(
                        perm,
                        class_name="inline-block text-[10px] font-medium px-1.5 py-0.5 bg-gray-100 text-gray-700 border border-gray-200 rounded",
                    ),
                ),
                class_name="flex flex-wrap gap-1",
            ),
            class_name="",
        ),
        class_name="bg-white border border-gray-200 rounded-lg p-4",
    )


def admin_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle_user_round", class_name="h-5 w-5 text-blue-600"
                    ),
                    rx.el.div(
                        rx.el.div(
                            "Current Session",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            "Role-aware permissions are enforced at the service layer",
                            class_name="text-xs text-gray-500",
                        ),
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            "User",
                            class_name="text-[10px] font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.div(
                            AuthState.current_user,
                            class_name="text-sm font-medium text-gray-900",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            "Role",
                            class_name="text-[10px] font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.div(
                            AuthState.current_role,
                            class_name="text-sm font-medium text-blue-600",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            "Permissions",
                            class_name="text-[10px] font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.div(
                            AuthState.current_permissions.length().to_string(),
                            class_name="text-sm font-medium text-gray-900",
                        ),
                    ),
                    class_name="flex items-center gap-8",
                ),
                class_name="flex items-center justify-between p-5",
            ),
            class_name="bg-white border border-gray-200 rounded-lg",
        ),
        rx.el.div(
            rx.el.div(
                "Available Roles",
                class_name="text-base font-semibold text-gray-900 mb-1",
            ),
            rx.el.div(
                "Switch role to preview permission scopes for the QC stock workflow",
                class_name="text-sm text-gray-500",
            ),
            class_name="mt-2",
        ),
        rx.el.div(
            rx.foreach(
                AuthState.available_roles,
                lambda r: role_card(r),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("info", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "Service Layer Rules",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
            ),
            rx.el.ul(
                rx.el.li(
                    rx.icon(
                        "check",
                        class_name="h-4 w-4 text-green-600 mt-0.5 shrink-0",
                    ),
                    rx.el.span(
                        "All stock-changing paths route through service-layer operations (issue, receive, adjust, transfer)."
                    ),
                    class_name="flex items-start gap-2 text-sm text-gray-700 py-2 border-b border-gray-100",
                ),
                rx.el.li(
                    rx.icon(
                        "check",
                        class_name="h-4 w-4 text-green-600 mt-0.5 shrink-0",
                    ),
                    rx.el.span(
                        "Negative stock is rejected without silent clamping; operations fail fast with explicit error messages."
                    ),
                    class_name="flex items-start gap-2 text-sm text-gray-700 py-2 border-b border-gray-100",
                ),
                rx.el.li(
                    rx.icon(
                        "check",
                        class_name="h-4 w-4 text-green-600 mt-0.5 shrink-0",
                    ),
                    rx.el.span(
                        "FEFO (First-Expiry-First-Out) lot selection is the default for issue/consume operations."
                    ),
                    class_name="flex items-start gap-2 text-sm text-gray-700 py-2 border-b border-gray-100",
                ),
                rx.el.li(
                    rx.icon(
                        "check",
                        class_name="h-4 w-4 text-green-600 mt-0.5 shrink-0",
                    ),
                    rx.el.span(
                        "Released-only stock is eligible for issue; Pending Release and Quarantine lots are filtered out."
                    ),
                    class_name="flex items-start gap-2 text-sm text-gray-700 py-2 border-b border-gray-100",
                ),
                rx.el.li(
                    rx.icon(
                        "check",
                        class_name="h-4 w-4 text-green-600 mt-0.5 shrink-0",
                    ),
                    rx.el.span(
                        "Every stock movement writes an immutable audit ledger entry with user, role, timestamp, and reason."
                    ),
                    class_name="flex items-start gap-2 text-sm text-gray-700 py-2",
                ),
                class_name="px-4 py-2",
            ),
            class_name="bg-white border border-gray-200 rounded-lg",
        ),
    )