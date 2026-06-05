import reflex as rx
from app.states.governance_state import GovernanceState


def expiry_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Open",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
            ),
            (
                "In Progress",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 w-fit",
            ),
            (
                "Completed",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200 w-fit",
            ),
            "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
        ),
    )


def expiry_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "calendar-clock", class_name="h-5 w-5 text-blue-600"
                    ),
                    rx.el.div(
                        rx.el.div(
                            "Expiry Check Tasks",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            f"{GovernanceState.open_expiry_tasks} open task(s)",
                            class_name="text-xs text-gray-500",
                        ),
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center justify-between p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Task #",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Item / Lot",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Expiry",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Days",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Assigned",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Action",
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
                        rx.foreach(
                            GovernanceState.expiry_tasks,
                            lambda t: rx.el.tr(
                                rx.el.td(
                                    t["task_no"],
                                    class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.div(
                                            t["item_name"],
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.div(
                                            t["lot_number"],
                                            class_name="text-[10px] font-mono text-gray-500",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    t["expiry_date"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        f"{t['days_to_expiry']}d",
                                        class_name=rx.cond(
                                            t["days_to_expiry"] <= 30,
                                            "text-xs font-semibold px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 w-fit",
                                            "text-xs font-semibold px-2 py-0.5 rounded-md bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    t["assigned_to"],
                                    class_name="text-sm text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    t["action"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    expiry_status_badge(t["status"]),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.cond(
                                        t["status"] != "Completed",
                                        rx.el.button(
                                            rx.icon(
                                                "check",
                                                class_name="h-3.5 w-3.5",
                                            ),
                                            "Complete",
                                            on_click=lambda: (
                                                GovernanceState.complete_expiry_task(
                                                    t["id"]
                                                )
                                            ),
                                            class_name="flex items-center gap-1 px-2 py-1 text-xs font-medium text-green-700 bg-green-50 hover:bg-green-100 border border-green-200 rounded-md",
                                        ),
                                        rx.el.span(
                                            t["completed_at"],
                                            class_name="text-[10px] text-gray-500",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                class_name="border-b border-gray-100 hover:bg-blue-50/30",
                            ),
                        ),
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
    )