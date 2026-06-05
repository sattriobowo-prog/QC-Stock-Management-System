import reflex as rx
from app.states.operations_state import OperationsState
from app.components.badges import status_badge


def receiving_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("circle_plus", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "New Receiving / PO Evidence",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Item",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option(
                            "Select an item…", value="", disabled=True
                        ),
                        rx.foreach(
                            OperationsState.item_options,
                            lambda o: rx.el.option(o["label"], value=o["id"]),
                        ),
                        value=OperationsState.rcv_item_id,
                        on_change=OperationsState.set_rcv_item,
                        class_name="appearance-none w-full pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-700 focus:outline-none focus:border-blue-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="col-span-3",
            ),
            rx.el.div(
                rx.el.label(
                    "PO Number",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="PO-2024-####",
                    default_value=OperationsState.rcv_po_number,
                    on_change=OperationsState.set_rcv_po.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Vendor",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Supplier name",
                    default_value=OperationsState.rcv_vendor,
                    on_change=OperationsState.set_rcv_vendor.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Lot Number",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Vendor lot / batch",
                    default_value=OperationsState.rcv_lot_number,
                    on_change=OperationsState.set_rcv_lot.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Quantity",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="0.00",
                    default_value=OperationsState.rcv_quantity,
                    on_change=OperationsState.set_rcv_quantity.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Expiry Date",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    type="date",
                    default_value=OperationsState.rcv_expiry,
                    on_change=OperationsState.set_rcv_expiry.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Document Reference (COA / Invoice)",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.div(
                    rx.icon(
                        "file-text",
                        class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="COA-####.pdf",
                        default_value=OperationsState.rcv_document_ref,
                        on_change=OperationsState.set_rcv_document.debounce(
                            300
                        ),
                        class_name="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                    ),
                    class_name="relative",
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.label(
                    "Notes",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.textarea(
                    placeholder="Receiving notes, COA results, condition, etc.",
                    default_value=OperationsState.rcv_notes,
                    on_change=OperationsState.set_rcv_notes.debounce(300),
                    rows="2",
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
                class_name="col-span-3",
            ),
            class_name="grid grid-cols-3 gap-3 px-4 py-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("info", class_name="h-3.5 w-3.5 text-blue-500"),
                rx.el.span(
                    "New lots default to Pending Release. Stock becomes available after QC release.",
                    class_name="text-xs text-blue-700",
                ),
                class_name="flex items-center gap-1.5 px-3 py-2 bg-blue-50 border border-blue-200 rounded-md",
            ),
            class_name="px-4 pb-3",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("circle_plus", class_name="h-4 w-4"),
                "Receive Lot",
                on_click=OperationsState.submit_receiving,
                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
            ),
            class_name="px-4 py-3 border-t border-gray-200 flex justify-end",
        ),
        class_name="bg-white border border-gray-200 rounded-lg",
    )


def receivings_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Receiving Records",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    f"{OperationsState.pending_release_count} pending release",
                    class_name="text-[10px] font-semibold px-2 py-0.5 ml-2 rounded bg-yellow-50 text-yellow-700 border border-yellow-200",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "GR #",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "PO",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Vendor",
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
                            "Received",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Expiry",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Document",
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
                        OperationsState.receivings,
                        lambda r: rx.el.tr(
                            rx.el.td(
                                r["receiving_no"],
                                class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                r["po_number"],
                                class_name="text-xs font-mono text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.td(
                                r["vendor"],
                                class_name="text-sm text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.div(
                                        r["item_name"],
                                        class_name="text-sm font-medium text-gray-900",
                                    ),
                                    rx.el.div(
                                        r["lot_number"],
                                        class_name="text-[10px] font-mono text-gray-500",
                                    ),
                                ),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                f"{r['quantity']} {r['unit']}",
                                class_name="text-sm text-gray-900 px-4 py-2.5 tabular-nums",
                            ),
                            rx.el.td(
                                r["received_date"],
                                class_name="text-xs text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.td(
                                r["expiry_date"],
                                class_name="text-xs text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.icon(
                                        "file-text",
                                        class_name="h-3.5 w-3.5 text-gray-400",
                                    ),
                                    rx.el.span(
                                        r["document_ref"],
                                        class_name="text-xs text-gray-700 truncate",
                                    ),
                                    class_name="flex items-center gap-1.5 max-w-[160px]",
                                ),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                status_badge(r["status"]),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.cond(
                                    r["status"] == "Pending Release",
                                    rx.el.button(
                                        rx.icon(
                                            "circle_check",
                                            class_name="h-3.5 w-3.5",
                                        ),
                                        "Release",
                                        on_click=lambda: (
                                            OperationsState.release_receiving(
                                                r["id"]
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


def receiving_view() -> rx.Component:
    return rx.fragment(
        receiving_form(),
        receivings_table(),
    )