import reflex as rx
from app.states.inventory_state import InventoryState
from app.components.badges import status_badge, hazard_badge, stock_level_badge


def info_row(label: str, value: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            label,
            class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
        ),
        rx.el.div(value, class_name="text-sm text-gray-900 mt-0.5"),
        class_name="flex flex-col py-2.5 border-b border-gray-100 last:border-b-0",
    )


def item_detail_view() -> rx.Component:
    item = InventoryState.selected_item
    return rx.fragment(
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="h-4 w-4"),
                "Back to Inventory",
                href="/inventory",
                class_name="inline-flex items-center gap-1.5 text-sm text-blue-600 hover:text-blue-700 font-medium",
            ),
            class_name="mb-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            item["name"],
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.div(
                            rx.el.span(
                                item["sku"],
                                class_name="text-xs font-mono px-2 py-0.5 bg-gray-100 text-gray-700 rounded border border-gray-200",
                            ),
                            rx.el.span(
                                f"Legacy: {item['legacy_code']}",
                                class_name="text-[10px] font-mono px-2 py-0.5 bg-gray-50 text-gray-500 rounded border border-gray-200",
                            ),
                            status_badge(item["status"]),
                            hazard_badge(item["is_hazard"], item["is_napza"]),
                            class_name="flex items-center gap-2 mt-2 flex-wrap",
                        ),
                        rx.el.p(
                            item["description"],
                            class_name="text-sm text-gray-600 mt-2",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("circle_minus", class_name="h-4 w-4"),
                            "Issue",
                            class_name="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 rounded-lg",
                        ),
                        rx.el.button(
                            rx.icon("circle_plus", class_name="h-4 w-4"),
                            "Receive",
                            class_name="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    class_name="flex items-start justify-between flex-wrap gap-3",
                ),
                class_name="bg-white border border-gray-200 rounded-lg p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "On Hand",
                        class_name="text-xs font-medium text-gray-500 uppercase",
                    ),
                    rx.el.div(
                        f"{item['on_hand']} ",
                        rx.el.span(
                            item["unit"],
                            class_name="text-sm text-gray-500 font-normal",
                        ),
                        class_name="text-3xl font-bold text-gray-900 mt-1",
                    ),
                    stock_level_badge(item["on_hand"], item["min_level"]),
                    class_name="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-2",
                ),
                rx.el.div(
                    rx.el.div(
                        "Reserved",
                        class_name="text-xs font-medium text-gray-500 uppercase",
                    ),
                    rx.el.div(
                        f"{item['reserved']} ",
                        rx.el.span(
                            item["unit"],
                            class_name="text-sm text-gray-500 font-normal",
                        ),
                        class_name="text-3xl font-bold text-orange-600 mt-1",
                    ),
                    rx.el.div(
                        "Allocated to requests",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-2",
                ),
                rx.el.div(
                    rx.el.div(
                        "Available",
                        class_name="text-xs font-medium text-gray-500 uppercase",
                    ),
                    rx.el.div(
                        f"{item['available']} ",
                        rx.el.span(
                            item["unit"],
                            class_name="text-sm text-gray-500 font-normal",
                        ),
                        class_name="text-3xl font-bold text-blue-600 mt-1",
                    ),
                    rx.el.div(
                        "Free for issue", class_name="text-xs text-gray-500"
                    ),
                    class_name="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-2",
                ),
                rx.el.div(
                    rx.el.div(
                        "Min / Max",
                        class_name="text-xs font-medium text-gray-500 uppercase",
                    ),
                    rx.el.div(
                        f"{item['min_level']} / {item['max_level']} ",
                        rx.el.span(
                            item["unit"],
                            class_name="text-sm text-gray-500 font-normal",
                        ),
                        class_name="text-3xl font-bold text-gray-900 mt-1",
                    ),
                    rx.el.div(
                        "Reorder thresholds", class_name="text-xs text-gray-500"
                    ),
                    class_name="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-2",
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("info", class_name="h-4 w-4 text-blue-500"),
                        rx.el.span(
                            "Item Information",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
                    ),
                    rx.el.div(
                        info_row("SKU", item["sku"]),
                        info_row("Legacy Code", item["legacy_code"]),
                        info_row("Category", item["category"]),
                        info_row("Unit of Measure", item["unit"]),
                        info_row("Default Vendor", item["vendor"]),
                        info_row("Storage Location", item["location"]),
                        info_row(
                            "Reorder Point",
                            f"{item['reorder_point']} {item['unit']}",
                        ),
                        info_row(
                            "Safety Stock",
                            f"{item['safety_stock']} {item['unit']}",
                        ),
                        info_row(
                            "Incoming",
                            f"{item['incoming']} {item['unit']}",
                        ),
                        info_row(
                            "Total Received (LTD)",
                            f"{item['total_received']} {item['unit']}",
                        ),
                        info_row(
                            "Total Issued (LTD)",
                            f"{item['total_issued']} {item['unit']}",
                        ),
                        info_row("Last Received", item["last_received_date"]),
                        info_row("Last Issued", item["last_issued_date"]),
                        info_row("Created", item["created_at"]),
                        info_row("Last Updated", item["last_updated"]),
                        class_name="px-4 py-2",
                    ),
                    class_name="bg-white border border-gray-200 rounded-lg",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("boxes", class_name="h-4 w-4 text-blue-500"),
                        rx.el.span(
                            "Lots for this Item",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
                    ),
                    rx.cond(
                        InventoryState.selected_item_lots.length() > 0,
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Lot #",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                                    ),
                                    rx.el.th(
                                        "Qty",
                                        class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2",
                                    ),
                                    rx.el.th(
                                        "Expiry",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                                    ),
                                    rx.el.th(
                                        "Status",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                                    ),
                                    class_name="bg-gray-50 border-b border-gray-200",
                                ),
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    InventoryState.selected_item_lots,
                                    lambda lot: rx.el.tr(
                                        rx.el.td(
                                            lot["lot_number"],
                                            class_name="text-xs font-mono text-gray-700 px-4 py-2",
                                        ),
                                        rx.el.td(
                                            f"{lot['quantity']} {lot['unit']}",
                                            class_name="text-sm text-gray-900 px-4 py-2 text-right tabular-nums",
                                        ),
                                        rx.el.td(
                                            lot["expiry_date"],
                                            class_name="text-sm text-gray-700 px-4 py-2",
                                        ),
                                        rx.el.td(
                                            status_badge(lot["status"]),
                                            class_name="px-4 py-2",
                                        ),
                                        class_name="border-b border-gray-100 hover:bg-gray-50 last:border-b-0",
                                    ),
                                ),
                            ),
                            class_name="table-auto w-full",
                        ),
                        rx.el.div(
                            "No lots associated with this item.",
                            class_name="px-4 py-6 text-sm text-gray-500 text-center",
                        ),
                    ),
                    class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
            ),
            class_name="flex flex-col gap-4",
        ),
    )