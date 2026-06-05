import reflex as rx
from app.states.inventory_state import InventoryState
from app.components.badges import status_badge, hazard_badge


def stock_priority_pill(p: rx.Var[int], label: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        label,
        class_name=rx.match(
            p,
            (
                1,
                "inline-flex px-2 py-0.5 rounded-md bg-red-100 text-red-800 border border-red-300 text-xs font-semibold w-fit",
            ),
            (
                2,
                "inline-flex px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 text-xs font-semibold w-fit",
            ),
            (
                3,
                "inline-flex px-2 py-0.5 rounded-md bg-orange-50 text-orange-700 border border-orange-200 text-xs font-semibold w-fit",
            ),
            (
                5,
                "inline-flex px-2 py-0.5 rounded-md bg-yellow-50 text-yellow-700 border border-yellow-200 text-xs font-semibold w-fit",
            ),
            "inline-flex px-2 py-0.5 rounded-md bg-green-50 text-green-700 border border-green-200 text-xs font-semibold w-fit",
        ),
    )


def filter_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                placeholder="Search by name, SKU, legacy code, category…",
                default_value=InventoryState.search_query,
                on_change=InventoryState.set_search.debounce(500),
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
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    InventoryState.locations,
                    lambda l: rx.el.option(l, value=l),
                ),
                value=InventoryState.location_filter,
                on_change=InventoryState.set_location,
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
                rx.el.option("Sort: Priority", value="priority"),
                rx.el.option("Sort: Name", value="name"),
                rx.el.option("Sort: Stock", value="stock"),
                value=InventoryState.sort_by,
                on_change=InventoryState.set_sort,
                class_name="appearance-none pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white text-gray-700",
            ),
            rx.icon(
                "chevron-down",
                class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="flex flex-wrap items-center gap-2 bg-white border border-gray-200 rounded-lg p-3",
    )


def summary_strip() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                "Showing",
                class_name="text-[10px] font-semibold text-gray-500 uppercase",
            ),
            rx.el.div(
                f"{InventoryState.filtered_items.length()} of {InventoryState.total_items}",
                class_name="text-sm font-bold text-gray-900",
            ),
            class_name="flex flex-col px-4 py-2",
        ),
        rx.el.div(
            rx.el.div(
                "Current Stock",
                class_name="text-[10px] font-semibold text-gray-500 uppercase",
            ),
            rx.el.div(
                InventoryState.total_current_stock_value.to_string(),
                class_name="text-sm font-bold text-blue-700",
            ),
            class_name="flex flex-col px-4 py-2 border-l border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                "Active 90d",
                class_name="text-[10px] font-semibold text-gray-500 uppercase",
            ),
            rx.el.div(
                InventoryState.total_active_90_value.to_string(),
                class_name="text-sm font-bold text-yellow-700",
            ),
            class_name="flex flex-col px-4 py-2 border-l border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                "Lots",
                class_name="text-[10px] font-semibold text-gray-500 uppercase",
            ),
            rx.el.div(
                InventoryState.total_lots.to_string(),
                class_name="text-sm font-bold text-gray-900",
            ),
            class_name="flex flex-col px-4 py-2 border-l border-gray-200",
        ),
        class_name="flex bg-white border border-gray-200 rounded-lg",
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
                        "Item",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Category",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Current",
                        class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Active 90d",
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
                        "Lots",
                        class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "Stock",
                        class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                    ),
                    rx.el.th(
                        "QC",
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
                    InventoryState.items_with_metrics,
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
                            f"{item['current_stock']} {item['unit']}",
                            class_name="text-sm font-semibold text-blue-700 px-4 py-2.5 text-right tabular-nums",
                        ),
                        rx.el.td(
                            f"{item['active_90']} {item['unit']}",
                            class_name="text-sm text-yellow-700 px-4 py-2.5 text-right tabular-nums",
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
                            item["lot_count"].to_string(),
                            class_name="text-sm text-gray-700 px-4 py-2.5 text-right tabular-nums",
                        ),
                        rx.el.td(
                            stock_priority_pill(
                                item["priority"], item["stock_status"]
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
    return rx.fragment(filter_bar(), summary_strip(), inventory_table())