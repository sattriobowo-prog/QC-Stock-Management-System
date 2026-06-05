import reflex as rx
from app.states.governance_state import GovernanceState
from app.states.auth_state import AuthState
from app.states.operations_state import OperationsState


def setting_row(s) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                s["label"], class_name="text-sm font-semibold text-gray-900"
            ),
            rx.el.div(
                s["description"], class_name="text-xs text-gray-500 mt-0.5"
            ),
            rx.el.span(
                s["category"],
                class_name="text-[10px] font-medium px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit mt-1",
            ),
            class_name="flex flex-col gap-0.5",
        ),
        rx.el.span(
            s["value"],
            class_name="text-xs font-semibold text-gray-900 px-2.5 py-1 bg-gray-100 rounded border border-gray-200 w-fit",
        ),
        class_name="flex items-center justify-between px-4 py-3 border-b border-gray-100 last:border-b-0",
    )


def md_request_row(m) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            m["request_no"],
            class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
        ),
        rx.el.td(m["entity"], class_name="text-xs text-gray-600 px-4 py-2.5"),
        rx.el.td(
            m["target"],
            class_name="text-sm font-medium text-gray-900 px-4 py-2.5",
        ),
        rx.el.td(
            m["change_type"], class_name="text-xs text-gray-700 px-4 py-2.5"
        ),
        rx.el.td(
            m["proposed_value"],
            class_name="text-xs text-blue-700 font-mono px-4 py-2.5",
        ),
        rx.el.td(
            m["requester"], class_name="text-sm text-gray-700 px-4 py-2.5"
        ),
        rx.el.td(
            rx.el.span(
                m["status"],
                class_name=rx.match(
                    m["status"],
                    (
                        "Pending Approval",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
                    ),
                    (
                        "Approved",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200 w-fit",
                    ),
                    (
                        "Rejected",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200 w-fit",
                    ),
                    "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
                ),
            ),
            class_name="px-4 py-2.5",
        ),
        rx.el.td(
            rx.cond(
                m["status"] == "Pending Approval",
                rx.el.div(
                    rx.el.button(
                        rx.icon("check", class_name="h-3.5 w-3.5"),
                        on_click=lambda: GovernanceState.approve_md_request(
                            m["id"]
                        ),
                        class_name="p-1.5 rounded-md text-green-600 hover:bg-green-50",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-3.5 w-3.5"),
                        on_click=lambda: GovernanceState.reject_md_request(
                            m["id"]
                        ),
                        class_name="p-1.5 rounded-md text-red-600 hover:bg-red-50",
                    ),
                    class_name="flex items-center gap-1",
                ),
                rx.fragment(),
            ),
            class_name="px-4 py-2.5",
        ),
        class_name="border-b border-gray-100 hover:bg-blue-50/30",
    )


def preserved_chip(label: str, kind: str) -> rx.Component:
    color = (
        "bg-green-50 text-green-700 border-green-200"
        if kind == "preserved"
        else "bg-red-50 text-red-700 border-red-200"
    )
    icon = "shield-check" if kind == "preserved" else "trash-2"
    return rx.el.div(
        rx.icon(icon, class_name="h-3 w-3"),
        rx.el.span(label, class_name="text-[11px] font-medium"),
        class_name=f"inline-flex items-center gap-1 px-2 py-0.5 rounded border {color} w-fit",
    )


def danger_zone() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("triangle-alert", class_name="h-4 w-4 text-red-500"),
            rx.el.span(
                "Danger Zone",
                class_name="text-sm font-semibold text-red-700",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-red-200 bg-red-50",
        ),
        rx.el.div(
            rx.el.div(
                "Operational Reset",
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.div(
                "Clears transactional data while preserving accounts, roles, vendors, items, lots master, document categories, and system settings. This action is irreversible and is restricted to the Admin role only.",
                class_name="text-xs text-gray-600 mt-1",
            ),
            rx.el.div(
                rx.el.div(
                    "Preserved",
                    class_name="text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1",
                ),
                rx.el.div(
                    preserved_chip("Users", "preserved"),
                    preserved_chip("Roles", "preserved"),
                    preserved_chip("Vendors", "preserved"),
                    preserved_chip("Items", "preserved"),
                    preserved_chip("Lots master", "preserved"),
                    preserved_chip("Settings", "preserved"),
                    preserved_chip("Doc categories", "preserved"),
                    class_name="flex flex-wrap gap-1",
                ),
                class_name="mt-3",
            ),
            rx.el.div(
                rx.el.div(
                    "Cleared",
                    class_name="text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1",
                ),
                rx.el.div(
                    preserved_chip("Material requests", "cleared"),
                    preserved_chip("Issues", "cleared"),
                    preserved_chip("Receivings", "cleared"),
                    preserved_chip("Adjustments", "cleared"),
                    preserved_chip("Transfers", "cleared"),
                    preserved_chip("Expiry tasks", "cleared"),
                    preserved_chip("Notifications", "cleared"),
                    preserved_chip("Audit log", "cleared"),
                    preserved_chip("MD requests", "cleared"),
                    class_name="flex flex-wrap gap-1",
                ),
                class_name="mt-3",
            ),
            rx.el.div(
                rx.icon(
                    "info",
                    class_name="h-3.5 w-3.5 text-orange-500 shrink-0",
                ),
                rx.el.span(
                    "Type RESET to enable the action button. Requires Admin role.",
                    class_name="text-xs text-orange-700",
                ),
                class_name="flex items-center gap-1.5 mt-3 px-3 py-2 bg-orange-50 border border-orange-200 rounded-md",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Type RESET to confirm",
                    default_value=GovernanceState.reset_confirm_text,
                    on_change=GovernanceState.set_reset_confirm.debounce(300),
                    class_name="flex-1 px-3 py-2 text-sm border border-red-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-red-500",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    "Reset Operations",
                    on_click=GovernanceState.perform_operational_reset,
                    disabled=(GovernanceState.reset_confirm_text != "RESET")
                    | (AuthState.current_role != "Admin"),
                    class_name=rx.cond(
                        (GovernanceState.reset_confirm_text == "RESET")
                        & (AuthState.current_role == "Admin"),
                        "flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg",
                        "flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-400 bg-gray-100 border border-gray-200 rounded-lg cursor-not-allowed",
                    ),
                ),
                class_name="flex items-center gap-2 mt-3",
            ),
            rx.cond(
                AuthState.current_role != "Admin",
                rx.el.div(
                    rx.icon("lock", class_name="h-3.5 w-3.5 text-red-500"),
                    rx.el.span(
                        f"Current role ({AuthState.current_role}) is not authorized for this action.",
                        class_name="text-xs text-red-700",
                    ),
                    class_name="flex items-center gap-1.5 mt-3 px-3 py-2 bg-red-50 border border-red-200 rounded-md",
                ),
                rx.fragment(),
            ),
            class_name="px-4 py-4",
        ),
        class_name="bg-white border-2 border-red-200 rounded-lg overflow-hidden",
    )


def settings_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.icon("settings", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "System Settings",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
            ),
            rx.foreach(GovernanceState.settings, setting_row),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-pen-line", class_name="h-4 w-4 text-blue-500"
                    ),
                    rx.el.span(
                        "Master Data Change Requests",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        f"{GovernanceState.pending_md_count} pending",
                        class_name="text-[10px] font-semibold px-2 py-0.5 ml-2 rounded bg-yellow-50 text-yellow-700 border border-yellow-200",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center justify-between px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Request #",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Entity",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Target",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Change",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Proposed",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Requester",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th("", class_name="px-4 py-2.5"),
                            class_name="bg-gray-50 border-b border-gray-200",
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(GovernanceState.md_requests, md_request_row)
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("scroll-text", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "Audit Trail",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(
                    OperationsState.audit_log,
                    lambda e: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                e["action"],
                                class_name="text-[10px] font-bold px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                            ),
                            rx.el.span(
                                e["target"],
                                class_name="text-xs font-mono text-gray-700",
                            ),
                            rx.el.span(
                                e["timestamp"],
                                class_name="text-xs text-gray-500 ml-auto",
                            ),
                            class_name="flex items-center gap-2 mb-1",
                        ),
                        rx.el.div(
                            e["detail"], class_name="text-sm text-gray-700"
                        ),
                        rx.el.div(
                            rx.icon("user", class_name="h-3 w-3 text-gray-400"),
                            rx.el.span(
                                f"{e['user']} ({e['role']})",
                                class_name="text-[10px] text-gray-500",
                            ),
                            class_name="flex items-center gap-1 mt-1",
                        ),
                        class_name="px-4 py-3 border-b border-gray-100 last:border-b-0",
                    ),
                ),
                class_name="max-h-96 overflow-y-auto",
            ),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
        danger_zone(),
    )