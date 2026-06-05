import reflex as rx
from app.states.inventory_state import InventoryState


def label_card(lot) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("flask-conical", class_name="h-4 w-4 text-blue-600"),
                rx.el.span(
                    "QC LAB", class_name="text-[10px] font-bold text-gray-700"
                ),
                class_name="flex items-center gap-1",
            ),
            rx.el.span(
                lot["status"],
                class_name=rx.match(
                    lot["status"],
                    (
                        "Released",
                        "text-[9px] font-bold px-1.5 py-0.5 rounded bg-green-100 text-green-800 border border-green-300",
                    ),
                    (
                        "Pending Release",
                        "text-[9px] font-bold px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-800 border border-yellow-300",
                    ),
                    (
                        "Quarantine",
                        "text-[9px] font-bold px-1.5 py-0.5 rounded bg-red-100 text-red-800 border border-red-300",
                    ),
                    "text-[9px] font-bold px-1.5 py-0.5 rounded bg-gray-100 text-gray-800 border border-gray-300",
                ),
            ),
            class_name="flex items-center justify-between mb-2 pb-2 border-b border-dashed border-gray-300",
        ),
        rx.el.div(
            lot["item_name"], class_name="text-sm font-bold text-gray-900 mb-1"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Lot:", class_name="text-[10px] text-gray-500"),
                rx.el.span(
                    lot["lot_number"],
                    class_name="text-xs font-mono text-gray-900 ml-1",
                ),
            ),
            rx.el.div(
                rx.el.span("Qty:", class_name="text-[10px] text-gray-500"),
                rx.el.span(
                    f"{lot['quantity']} {lot['unit']}",
                    class_name="text-xs font-medium text-gray-900 ml-1",
                ),
            ),
            rx.el.div(
                rx.el.span("Recv:", class_name="text-[10px] text-gray-500"),
                rx.el.span(
                    lot["received_date"],
                    class_name="text-xs text-gray-700 ml-1",
                ),
            ),
            rx.el.div(
                rx.el.span("Exp:", class_name="text-[10px] text-gray-500"),
                rx.el.span(
                    lot["expiry_date"],
                    class_name="text-xs font-semibold text-red-700 ml-1",
                ),
            ),
            class_name="grid grid-cols-2 gap-1 mb-2",
        ),
        rx.el.div(
            rx.icon("qr-code", class_name="h-12 w-12 text-gray-700 mx-auto"),
            rx.el.div(
                lot["lot_number"],
                class_name="text-[9px] font-mono text-center text-gray-500 mt-1",
            ),
            class_name="border-t border-dashed border-gray-300 pt-2",
        ),
        class_name="bg-white border-2 border-gray-300 rounded-lg p-3 w-full",
    )


def labels_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.icon("tag", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "Lot Labels",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    "Print or export QR-coded labels for each lot",
                    class_name="text-xs text-gray-500 ml-2",
                ),
                class_name="flex items-center px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("printer", class_name="h-4 w-4"),
                    "Print Selected",
                    class_name="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 rounded-lg",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4"),
                    "Export PDF",
                    class_name="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
                ),
                class_name="flex items-center gap-2 px-4 py-3 bg-gray-50 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(InventoryState.lots, label_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 p-4",
            ),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
    )