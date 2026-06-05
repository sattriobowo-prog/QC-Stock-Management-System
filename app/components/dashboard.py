import reflex as rx
from app.states.inventory_state import InventoryState
from app.components.badges import status_badge, hazard_badge, stock_level_badge


def stat_card(
    label: str, value: rx.Var, icon: str, accent: str, hint: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"h-5 w-5 {accent}"),
                class_name=f"p-2 rounded-lg bg-gray-50 border border-gray-200 w-fit",
            ),
            rx.el.div(
                rx.el.div(
                    label,
                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
                ),
                rx.el.div(
                    value, class_name="text-2xl font-bold text-gray-900 mt-1"
                ),
                rx.el.div(hint, class_name="text-xs text-gray-500 mt-1"),
            ),
            class_name="flex items-start gap-4",
        ),
        class_name="bg-white border border-gray-200 rounded-lg p-5 hover:border-blue-300 transition-colors",
    )


def alert_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("triangle-alert", class_name="h-4 w-4 text-orange-500"),
                rx.el.span(
                    "Stock Alerts",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.span(
                "Live",
                class_name="text-[10px] font-medium px-1.5 py-0.5 bg-green-50 text-green-700 border border-green-200 rounded w-fit",
            ),
            class_name="flex items-center justify-between px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(
                InventoryState.items,
                lambda item: rx.cond(
                    item["on_hand"] < item["min_level"],
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                rx.cond(
                                    item["on_hand"] <= 0,
                                    "circle-x",
                                    "triangle-alert",
                                ),
                                class_name=rx.cond(
                                    item["on_hand"] <= 0,
                                    "h-4 w-4 text-red-500",
                                    "h-4 w-4 text-orange-500",
                                ),
                            ),
                            rx.el.div(
                                rx.el.div(
                                    item["name"],
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                rx.el.div(
                                    f"On hand: {item['on_hand']} {item['unit']} • Min: {item['min_level']} {item['unit']}",
                                    class_name="text-xs text-gray-500",
                                ),
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        stock_level_badge(item["on_hand"], item["min_level"]),
                        class_name="flex items-center justify-between px-4 py-3 border-b border-gray-100 last:border-b-0 hover:bg-gray-50",
                    ),
                    rx.fragment(),
                ),
            ),
            class_name="divide-y divide-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def expiry_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("calendar-clock", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Expiring Lots (90 days)",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(
                InventoryState.lots,
                lambda lot: rx.cond(
                    (lot["days_to_expiry"] <= 90)
                    & (lot["days_to_expiry"] >= 0),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                lot["item_name"],
                                class_name="text-sm font-medium text-gray-900",
                            ),
                            rx.el.div(
                                f"Lot: {lot['lot_number']} • Exp: {lot['expiry_date']}",
                                class_name="text-xs text-gray-500",
                            ),
                        ),
                        rx.el.span(
                            f"{lot['days_to_expiry']}d",
                            class_name=rx.cond(
                                lot["days_to_expiry"] <= 30,
                                "text-xs font-semibold px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 w-fit",
                                "text-xs font-semibold px-2 py-0.5 rounded-md bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
                            ),
                        ),
                        class_name="flex items-center justify-between px-4 py-3 border-b border-gray-100 last:border-b-0 hover:bg-gray-50",
                    ),
                    rx.fragment(),
                ),
            ),
            class_name="divide-y divide-gray-100 max-h-80 overflow-y-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def recent_items_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("activity", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Recently Updated Items",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Code",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                        ),
                        rx.el.th(
                            "Item",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                        ),
                        rx.el.th(
                            "On Hand",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                        ),
                        rx.el.th(
                            "Updated",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2",
                        ),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        InventoryState.items,
                        lambda item: rx.el.tr(
                            rx.el.td(
                                item["sku"],
                                class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.span(
                                        item["name"],
                                        class_name="text-sm text-gray-900",
                                    ),
                                    hazard_badge(
                                        item["is_hazard"], item["is_napza"]
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                f"{item['on_hand']} {item['unit']}",
                                class_name="text-sm text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                status_badge(item["status"]),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                item["last_updated"],
                                class_name="text-xs text-gray-500 px-4 py-2.5",
                            ),
                            class_name="border-b border-gray-100 hover:bg-gray-50",
                        ),
                    ),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def dashboard_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            stat_card(
                "Total Items",
                InventoryState.total_items.to_string(),
                "package",
                "text-blue-600",
                "Active SKUs in catalog",
            ),
            stat_card(
                "Low Stock",
                InventoryState.low_stock_count.to_string(),
                "triangle-alert",
                "text-orange-600",
                "Below minimum level",
            ),
            stat_card(
                "Out of Stock",
                InventoryState.out_of_stock_count.to_string(),
                "circle-x",
                "text-red-600",
                "Requires immediate action",
            ),
            stat_card(
                "Expiring Soon",
                InventoryState.expiring_soon_count.to_string(),
                "calendar-clock",
                "text-yellow-600",
                "Within next 90 days",
            ),
            stat_card(
                "NAPZA Items",
                InventoryState.napza_count.to_string(),
                "shield-alert",
                "text-purple-600",
                "Controlled substances",
            ),
            stat_card(
                "Active Lots",
                InventoryState.total_lots.to_string(),
                "boxes",
                "text-green-600",
                "Tracked batches",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4",
        ),
        rx.el.div(
            alert_card(),
            expiry_card(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
        ),
        recent_items_card(),
    )