import reflex as rx
from app.states.operations_state import OperationsState
from app.states.auth_state import AuthState


def adj_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Approved",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200 w-fit",
            ),
            (
                "Pending Approval",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
            ),
            (
                "Rejected",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200 w-fit",
            ),
            "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
        ),
    )


def adjustment_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("settings-2", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Submit Adjustment",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Item",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option(
                            "Select an item…", value="", disabled=True
                        ),
                        rx.foreach(
                            OperationsState.item_options,
                            lambda o: rx.el.option(o["label"], value=o["id"]),
                        ),
                        value=OperationsState.adj_item_id,
                        on_change=OperationsState.set_adj_item,
                        class_name="appearance-none w-full pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-700 focus:outline-none focus:border-blue-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.label(
                    "Delta (+/-)",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="e.g. -1.5 or 5",
                    default_value=OperationsState.adj_delta,
                    on_change=OperationsState.set_adj_delta.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Reason",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Spillage / Breakage / Cycle count / etc.",
                    default_value=OperationsState.adj_reason,
                    on_change=OperationsState.set_adj_reason.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.label(
                    "Notes",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.textarea(
                    placeholder="Incident report, supporting evidence, etc.",
                    default_value=OperationsState.adj_notes,
                    on_change=OperationsState.set_adj_notes.debounce(300),
                    rows="2",
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
                class_name="col-span-3",
            ),
            class_name="grid grid-cols-3 gap-3 px-4 py-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "shield-alert", class_name="h-3.5 w-3.5 text-orange-500"
                ),
                rx.el.span(
                    "Self-approval is blocked. A different role must approve this adjustment.",
                    class_name="text-xs text-orange-700",
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.button(
                rx.icon("send", class_name="h-4 w-4"),
                "Submit for Approval",
                on_click=OperationsState.submit_adjustment,
                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
            ),
            class_name="flex items-center justify-between px-4 py-3 border-t border-gray-200",
        ),
        class_name="bg-white border border-gray-200 rounded-lg",
    )


def adjustment_row(a: rx.Var) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            a["adjustment_no"],
            class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
        ),
        rx.el.td(
            a["item_name"],
            class_name="text-sm font-medium text-gray-900 px-4 py-2.5",
        ),
        rx.el.td(
            rx.el.span(
                f"{a['delta']} {a['unit']}",
                class_name=rx.cond(
                    a["delta"] < 0,
                    "text-sm font-semibold text-red-600 tabular-nums",
                    "text-sm font-semibold text-green-600 tabular-nums",
                ),
            ),
            class_name="px-4 py-2.5",
        ),
        rx.el.td(
            a["reason"],
            class_name="text-xs text-gray-600 px-4 py-2.5 max-w-xs truncate",
        ),
        rx.el.td(
            a["submitter"], class_name="text-sm text-gray-700 px-4 py-2.5"
        ),
        rx.el.td(a["approver"], class_name="text-sm text-gray-700 px-4 py-2.5"),
        rx.el.td(adj_status_badge(a["status"]), class_name="px-4 py-2.5"),
        rx.el.td(
            a["created_at"], class_name="text-xs text-gray-500 px-4 py-2.5"
        ),
        rx.el.td(
            rx.cond(
                a["status"] == "Pending Approval",
                rx.cond(
                    a["submitter"] == AuthState.current_user,
                    rx.el.span(
                        "Self-submitted",
                        class_name="text-[10px] font-medium text-gray-400 italic",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("check", class_name="h-3.5 w-3.5"),
                            on_click=lambda: OperationsState.approve_adjustment(
                                a["id"]
                            ),
                            class_name="p-1.5 rounded-md text-green-600 hover:bg-green-50",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-3.5 w-3.5"),
                            on_click=lambda: OperationsState.reject_adjustment(
                                a["id"]
                            ),
                            class_name="p-1.5 rounded-md text-red-600 hover:bg-red-50",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                ),
                rx.fragment(),
            ),
            class_name="px-4 py-2.5",
        ),
        class_name="border-b border-gray-100 hover:bg-blue-50/30",
    )


def adjustments_table(title: str, items_var, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-blue-500"),
            rx.el.span(title, class_name="text-sm font-semibold text-gray-900"),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Adj #",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Item",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Delta",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Reason",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Submitter",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Approver",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Created",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th("", class_name="px-4 py-2.5"),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(items_var, adjustment_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def audit_log_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("scroll-text", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Recent Audit Trail",
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
                    rx.el.div(e["detail"], class_name="text-sm text-gray-700"),
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
    )


def adjustments_view() -> rx.Component:
    return rx.fragment(
        adjustment_form(),
        adjustments_table(
            "All Adjustments", OperationsState.adjustments, "list-checks"
        ),
        audit_log_card(),
    )