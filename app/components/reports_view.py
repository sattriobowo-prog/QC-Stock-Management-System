import reflex as rx
from app.states.inventory_state import InventoryState
from app.states.operations_state import OperationsState
from app.states.governance_state import GovernanceState


def report_card(
    label: str, value: rx.Var, hint: str, icon: str, accent: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 {accent}"),
            class_name="p-2 rounded-lg bg-gray-50 border border-gray-200 w-fit",
        ),
        rx.el.div(
            rx.el.div(
                label,
                class_name="text-xs font-medium text-gray-500 uppercase tracking-wide mt-3",
            ),
            rx.el.div(
                value, class_name="text-2xl font-bold text-gray-900 mt-1"
            ),
            rx.el.div(hint, class_name="text-xs text-gray-500 mt-1"),
        ),
        class_name="bg-white border border-gray-200 rounded-lg p-5",
    )


def reports_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            report_card(
                "Total SKUs",
                InventoryState.total_items.to_string(),
                "Active catalog",
                "package",
                "text-blue-600",
            ),
            report_card(
                "Active Lots",
                InventoryState.total_lots.to_string(),
                "Tracked batches",
                "boxes",
                "text-green-600",
            ),
            report_card(
                "Expiring (90d)",
                InventoryState.expiring_soon_count.to_string(),
                "Risk window",
                "calendar-clock",
                "text-yellow-600",
            ),
            report_card(
                "Low Stock",
                InventoryState.low_stock_count.to_string(),
                "Below minimum",
                "triangle-alert",
                "text-orange-600",
            ),
            report_card(
                "Out of Stock",
                InventoryState.out_of_stock_count.to_string(),
                "Reorder needed",
                "circle-x",
                "text-red-600",
            ),
            report_card(
                "NAPZA SKUs",
                InventoryState.napza_count.to_string(),
                "Controlled",
                "shield-alert",
                "text-purple-600",
            ),
            report_card(
                "Pending MR",
                OperationsState.pending_request_count.to_string(),
                "Awaiting approval",
                "clipboard-list",
                "text-blue-600",
            ),
            report_card(
                "Pending Adj.",
                OperationsState.pending_adjustment_count.to_string(),
                "Awaiting approval",
                "settings-2",
                "text-orange-600",
            ),
            report_card(
                "Pending Release",
                OperationsState.pending_release_count.to_string(),
                "Receiving lots",
                "circle_plus",
                "text-yellow-600",
            ),
            report_card(
                "Active Vendors",
                GovernanceState.active_vendor_count.to_string(),
                "Qualified suppliers",
                "truck",
                "text-green-600",
            ),
            report_card(
                "Open Expiry Tasks",
                GovernanceState.open_expiry_tasks.to_string(),
                "Action required",
                "alarm-clock",
                "text-red-600",
            ),
            report_card(
                "Pending Transfers",
                GovernanceState.pending_transfer_count.to_string(),
                "Internal moves",
                "arrow-right-left",
                "text-blue-600",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("bar-chart-3", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "Stock Levels by Item",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(
                    InventoryState.items,
                    lambda i: rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                i["name"],
                                class_name="text-sm font-medium text-gray-900",
                            ),
                            rx.el.div(
                                f"{i['on_hand']} / {i['max_level']} {i['unit']}",
                                class_name="text-xs text-gray-500 tabular-nums",
                            ),
                            class_name="flex items-center justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name=rx.cond(
                                    i["on_hand"] <= 0,
                                    "h-2 rounded-full bg-red-500",
                                    rx.cond(
                                        i["on_hand"] < i["min_level"],
                                        "h-2 rounded-full bg-orange-500",
                                        "h-2 rounded-full bg-blue-500",
                                    ),
                                ),
                                style={
                                    "width": rx.cond(
                                        i["max_level"] > 0,
                                        (
                                            i["on_hand"] / i["max_level"] * 100
                                        ).to_string()
                                        + "%",
                                        "0%",
                                    )
                                },
                            ),
                            class_name="w-full h-2 bg-gray-100 rounded-full overflow-hidden",
                        ),
                        class_name="px-4 py-3 border-b border-gray-100 last:border-b-0",
                    ),
                ),
                class_name="max-h-96 overflow-y-auto",
            ),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
    )