import reflex as rx
from app.states.governance_state import GovernanceState


def transfer_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Pending",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
            ),
            (
                "Completed",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200 w-fit",
            ),
            (
                "Rejected",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200 w-fit",
            ),
            "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
        ),
    )


def transfers_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("arrow-right-left", class_name="h-5 w-5 text-blue-600"),
                rx.el.div(
                    rx.el.div(
                        "Internal Transfers",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.div(
                        f"{GovernanceState.pending_transfer_count} pending transfer(s)",
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
                            "Transfer #",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Item / Lot",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Qty",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "From → To",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Reason",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Requested",
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
                        GovernanceState.transfers,
                        lambda t: rx.el.tr(
                            rx.el.td(
                                t["transfer_no"],
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
                                f"{t['quantity']} {t['unit']}",
                                class_name="text-sm text-gray-900 px-4 py-2.5 tabular-nums",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.span(
                                        t["from_location"],
                                        class_name="text-xs text-gray-700",
                                    ),
                                    rx.icon(
                                        "arrow-right",
                                        class_name="h-3 w-3 text-gray-400 mx-1 inline",
                                    ),
                                    rx.el.span(
                                        t["to_location"],
                                        class_name="text-xs text-blue-700 font-medium",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                t["reason"],
                                class_name="text-xs text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.div(
                                        t["requested_by"],
                                        class_name="text-sm text-gray-700",
                                    ),
                                    rx.el.div(
                                        t["created_at"],
                                        class_name="text-xs text-gray-500",
                                    ),
                                ),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                transfer_status_badge(t["status"]),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.cond(
                                    t["status"] == "Pending",
                                    rx.el.button(
                                        rx.icon(
                                            "check", class_name="h-3.5 w-3.5"
                                        ),
                                        "Approve",
                                        on_click=lambda: (
                                            GovernanceState.approve_transfer(
                                                t["id"]
                                            )
                                        ),
                                        class_name="flex items-center gap-1 px-2 py-1 text-xs font-medium text-green-700 bg-green-50 hover:bg-green-100 border border-green-200 rounded-md",
                                    ),
                                    rx.fragment(),
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
    )