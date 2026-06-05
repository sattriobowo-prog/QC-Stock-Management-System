import reflex as rx
from app.states.inventory_state import InventoryState
from app.components.badges import status_badge, hazard_badge, stock_level_badge


def filter_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                placeholder="Search by name, code, or category...",
                default_value=InventoryState.search_query,
                on_change=InventoryState.set_search.debounce(300),
                class_name="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white text-gray-900 placeholder-gray-400",
            ),
            class_name="relative flex-1 min-w-[260px]",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    InventoryState.categories,
                    lambda c: rx.el.option(c, value=c),
                ),
                value=InventoryState.category_filter,
                on_change=InventoryState.set_category,
                class_name="appearance-none pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white text-gray-700",
            ),
            rx.icon(
                "chevron-down",
                class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    InventoryState.statuses,
                    lambda s: rx.el.option(s, value=s),
                ),
                value=InventoryState.status_filter,
                on_change=InventoryState.set_status,
                class_name="appearance-none pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white text-gray-700",
            ),
            rx.icon(
                "chevron-down",
                class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "New Item",
            class_name="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors",
        ),
        class_name="flex flex-wrap items-center gap-2 bg-white border border-gray-200 rounded-lg p-3",
    )


def inventory_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "SKU",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Item Name",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Category",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "On Hand",
                        class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Available",
                        class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Min",
                        class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Level",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Status",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Location",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Flags",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th("", class_name="px-4 py-2.5"),
                    class_name="bg-gray-50 border-b border-gray-200",
                ),
            ),
            rx.el.tbody(
                rx.foreach(
                    InventoryState.filtered_items,
                    lambda item: rx.el.tr(
                        rx.el.td(
                            rx.el.div(
                                rx.el.div(
                                    item["sku"],
                                    class_name="text-xs font-mono text-gray-900",
                                ),
                                rx.el.div(
                                    item["legacy_code"],
                                    class_name="text-[10px] font-mono text-gray-400",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="px-4 py-2.5",
                        ),
                        rx.el.td(
                            rx.el.div(
                                rx.el.div(
                                    item["name"],
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                rx.el.div(
                                    item["description"],
                                    class_name="text-xs text-gray-500 truncate max-w-xs",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="px-4 py-2.5",
                        ),
                        rx.el.td(
                            item["category"],
                            class_name="text-sm text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.td(
                            f"{item['on_hand']} {item['unit']}",
                            class_name="text-sm text-gray-900 px-4 py-2.5 text-right tabular-nums",
                        ),
                        rx.el.td(
                            f"{item['available']} {item['unit']}",
                            class_name="text-sm text-gray-700 px-4 py-2.5 text-right tabular-nums",
                        ),
                        rx.el.td(
                            f"{item['min_level']}",
                            class_name="text-xs text-gray-500 px-4 py-2.5 text-right tabular-nums",
                        ),
                        rx.el.td(
                            stock_level_badge(
                                item["on_hand"], item["min_level"]
                            ),
                            class_name="px-4 py-2.5",
                        ),
                        rx.el.td(
                            status_badge(item["status"]),
                            class_name="px-4 py-2.5",
                        ),
                        rx.el.td(
                            item["location"],
                            class_name="text-xs text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.td(
                            hazard_badge(item["is_hazard"], item["is_napza"]),
                            class_name="px-4 py-2.5",
                        ),
                        rx.el.td(
                            rx.el.button(
                                rx.icon("arrow-right", class_name="h-4 w-4"),
                                on_click=lambda: InventoryState.select_item(
                                    item["id"]
                                ),
                                class_name="p-1.5 rounded-md text-gray-500 hover:bg-blue-50 hover:text-blue-600 transition-colors",
                            ),
                            class_name="px-4 py-2.5",
                        ),
                        class_name="border-b border-gray-100 hover:bg-blue-50/30 transition-colors",
                    ),
                ),
            ),
            class_name="table-auto w-full",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-x-auto",
    )


def inventory_view() -> rx.Component:
    return rx.fragment(filter_bar(), inventory_table())