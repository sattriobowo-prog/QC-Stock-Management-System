import reflex as rx
from app.states.inventory_state import InventoryState
from app.components.badges import status_badge


def expiry_indicator(days: rx.Var[int]) -> rx.Component:
    return rx.cond(
        days < 0,
        rx.el.span(
            "Expired",
            class_name="inline-flex items-center px-2 py-0.5 rounded-md bg-red-100 text-red-800 border border-red-300 text-xs font-semibold w-fit",
        ),
        rx.cond(
            days <= 30,
            rx.el.span(
                f"{days}d",
                class_name="inline-flex items-center px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 text-xs font-semibold w-fit",
            ),
            rx.cond(
                days <= 90,
                rx.el.span(
                    f"{days}d",
                    class_name="inline-flex items-center px-2 py-0.5 rounded-md bg-yellow-50 text-yellow-700 border border-yellow-200 text-xs font-semibold w-fit",
                ),
                rx.el.span(
                    f"{days}d",
                    class_name="inline-flex items-center px-2 py-0.5 rounded-md bg-green-50 text-green-700 border border-green-200 text-xs font-semibold w-fit",
                ),
            ),
        ),
    )


def location_rollup_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("map-pin", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Stock Balance Rollup by Location",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(
                InventoryState.location_balances,
                lambda lb: rx.el.div(
                    rx.el.div(
                        rx.icon("map-pin", class_name="h-4 w-4 text-gray-400"),
                        rx.el.div(
                            lb["location"],
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        class_name="flex items-center gap-2 mb-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                "Lots",
                                class_name="text-[10px] font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.div(
                                lb["lots"].to_string(),
                                class_name="text-lg font-bold text-blue-700",
                            ),
                        ),
                        rx.el.div(
                            rx.el.div(
                                "Items",
                                class_name="text-[10px] font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.div(
                                lb["item_count"].to_string(),
                                class_name="text-lg font-bold text-gray-900",
                            ),
                        ),
                        rx.el.div(
                            rx.el.div(
                                "Total Qty",
                                class_name="text-[10px] font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.div(
                                lb["quantity"].to_string(),
                                class_name="text-lg font-bold text-yellow-700",
                            ),
                        ),
                        class_name="grid grid-cols-3 gap-2",
                    ),
                    class_name="p-3 border border-gray-200 rounded-lg bg-white",
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 p-4",
        ),
        class_name="bg-white border border-gray-200 rounded-lg",
    )


def lots_view() -> rx.Component:
    return rx.fragment(
        location_rollup_card(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("boxes", class_name="h-5 w-5 text-blue-600"),
                    rx.el.div(
                        rx.el.div(
                            "All Lots & Batches",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            "FEFO-ordered batch tracking with expiry monitoring",
                            class_name="text-xs text-gray-500",
                        ),
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{InventoryState.total_lots} lots",
                        class_name="text-xs font-medium text-gray-600 px-2.5 py-1 bg-gray-100 rounded-md border border-gray-200",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center justify-between p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Lot Number",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Item",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Qty",
                                class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Received",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Expiry",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "To Expiry",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Vendor",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Location",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "QC Status",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            class_name="bg-gray-50 border-b border-gray-200",
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            InventoryState.lots,
                            lambda lot: rx.el.tr(
                                rx.el.td(
                                    lot["lot_number"],
                                    class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    lot["item_name"],
                                    class_name="text-sm font-medium text-gray-900 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    f"{lot['quantity']} {lot['unit']}",
                                    class_name="text-sm text-gray-900 px-4 py-2.5 text-right tabular-nums",
                                ),
                                rx.el.td(
                                    lot["received_date"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    lot["expiry_date"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    expiry_indicator(lot["days_to_expiry"]),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    lot["vendor"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    lot["location"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    status_badge(lot["status"]),
                                    class_name="px-4 py-2.5",
                                ),
                                class_name="border-b border-gray-100 hover:bg-blue-50/30 last:border-b-0",
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