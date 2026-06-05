import reflex as rx
from app.states.inventory_state import InventoryState


def scan_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.icon("scan-line", class_name="h-5 w-5 text-blue-600"),
                rx.el.div(
                    rx.el.div(
                        "Scan & Lookup",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.div(
                        "Scan a barcode, QR code, or SKU to look up an item, lot, or location.",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-3 p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("qr-code", class_name="h-24 w-24 text-gray-300"),
                    rx.el.div(
                        "Scanner ready",
                        class_name="text-sm font-medium text-gray-600 mt-3",
                    ),
                    rx.el.div(
                        "Type or paste a code below, or use a connected USB scanner.",
                        class_name="text-xs text-gray-500 mt-1 text-center max-w-sm",
                    ),
                    class_name="flex flex-col items-center justify-center py-12 bg-gray-50 border border-dashed border-gray-300 rounded-lg",
                ),
                rx.el.div(
                    rx.el.label(
                        "Quick Lookup",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Scan or type SKU / Lot / Code…",
                            default_value=InventoryState.search_query,
                            on_change=InventoryState.set_search.debounce(300),
                            class_name="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white",
                        ),
                        class_name="relative",
                    ),
                    class_name="mt-4",
                ),
                rx.cond(
                    InventoryState.search_query != "",
                    rx.el.div(
                        rx.el.div(
                            f"{InventoryState.filtered_items.length()} match(es)",
                            class_name="text-xs font-medium text-gray-500 mt-3 mb-2",
                        ),
                        rx.foreach(
                            InventoryState.filtered_items,
                            lambda i: rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        i["name"],
                                        class_name="text-sm font-semibold text-gray-900",
                                    ),
                                    rx.el.div(
                                        f"{i['sku']} • {i['category']} • {i['location']}",
                                        class_name="text-xs text-gray-500",
                                    ),
                                ),
                                rx.el.button(
                                    rx.icon(
                                        "arrow-right", class_name="h-4 w-4"
                                    ),
                                    on_click=lambda: InventoryState.select_item(
                                        i["id"]
                                    ),
                                    class_name="p-1.5 rounded-md text-blue-600 hover:bg-blue-50",
                                ),
                                class_name="flex items-center justify-between px-3 py-2 border border-gray-200 rounded-lg mb-2 hover:bg-blue-50/30",
                            ),
                        ),
                        class_name="",
                    ),
                    rx.fragment(),
                ),
                class_name="p-4",
            ),
            class_name="bg-white border border-gray-200 rounded-lg",
        ),
    )