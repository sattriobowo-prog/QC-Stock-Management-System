import reflex as rx
from app.states.inventory_state import InventoryState
from app.states.operations_state import OperationsState
from app.states.governance_state import GovernanceState
from app.components.badges import status_badge, hazard_badge


def info_row(label: str, value: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            label,
            class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
        ),
        rx.el.div(value, class_name="text-sm text-gray-900 mt-0.5"),
        class_name="flex flex-col py-2.5 border-b border-gray-100 last:border-b-0",
    )


def tab_button(label: str, tab_id: str, icon: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label, class_name="text-sm font-medium"),
        on_click=lambda: InventoryState.set_detail_tab(tab_id),
        class_name=rx.cond(
            InventoryState.detail_tab == tab_id,
            "flex items-center gap-2 px-4 py-2.5 border-b-2 border-blue-600 text-blue-700 bg-blue-50/40",
            "flex items-center gap-2 px-4 py-2.5 border-b-2 border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50",
        ),
    )


def overview_tab() -> rx.Component:
    item = InventoryState.selected_item
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Current Stock",
                    class_name="text-xs font-medium text-gray-500 uppercase",
                ),
                rx.el.div(
                    f"{InventoryState.selected_item_current_stock} ",
                    rx.el.span(
                        item["unit"],
                        class_name="text-sm text-gray-500 font-normal",
                    ),
                    class_name="text-3xl font-bold text-blue-700 mt-1",
                ),
                rx.el.div(
                    "Released lots only",
                    class_name="text-xs text-gray-500",
                ),
                class_name="bg-white border border-gray-200 rounded-lg p-5",
            ),
            rx.el.div(
                rx.el.div(
                    "Active 90d",
                    class_name="text-xs font-medium text-gray-500 uppercase",
                ),
                rx.el.div(
                    f"{InventoryState.selected_item_active_90} ",
                    rx.el.span(
                        item["unit"],
                        class_name="text-sm text-gray-500 font-normal",
                    ),
                    class_name="text-3xl font-bold text-yellow-700 mt-1",
                ),
                rx.el.div(
                    "Expiring within 90 days",
                    class_name="text-xs text-gray-500",
                ),
                class_name="bg-white border border-gray-200 rounded-lg p-5",
            ),
            rx.el.div(
                rx.el.div(
                    "On Hand / Available",
                    class_name="text-xs font-medium text-gray-500 uppercase",
                ),
                rx.el.div(
                    f"{item['on_hand']} / {item['available']} ",
                    rx.el.span(
                        item["unit"],
                        class_name="text-sm text-gray-500 font-normal",
                    ),
                    class_name="text-2xl font-bold text-gray-900 mt-1",
                ),
                rx.el.div(
                    f"Reserved: {item['reserved']} {item['unit']}",
                    class_name="text-xs text-gray-500",
                ),
                class_name="bg-white border border-gray-200 rounded-lg p-5",
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
                    class_name="text-2xl font-bold text-gray-900 mt-1",
                ),
                rx.el.div(
                    InventoryState.selected_item_status_label,
                    class_name="text-xs font-semibold text-blue-700",
                ),
                class_name="bg-white border border-gray-200 rounded-lg p-5",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4",
        ),
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
                    "Reorder Point", f"{item['reorder_point']} {item['unit']}"
                ),
                info_row(
                    "Safety Stock", f"{item['safety_stock']} {item['unit']}"
                ),
                info_row("Incoming", f"{item['incoming']} {item['unit']}"),
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
    )


def sources_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("truck", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Vendor Sources",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.cond(
            InventoryState.selected_item_sources.length() > 0,
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Vendor",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Lots Supplied",
                            class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Total Quantity",
                            class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Last Received",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        InventoryState.selected_item_sources,
                        lambda s: rx.el.tr(
                            rx.el.td(
                                s["vendor"],
                                class_name="text-sm font-medium text-gray-900 px-4 py-2.5",
                            ),
                            rx.el.td(
                                s["lot_count"].to_string(),
                                class_name="text-sm text-gray-700 px-4 py-2.5 text-right tabular-nums",
                            ),
                            rx.el.td(
                                f"{s['total_qty']} {s['unit']}",
                                class_name="text-sm text-blue-700 font-semibold px-4 py-2.5 text-right tabular-nums",
                            ),
                            rx.el.td(
                                s["last_received"],
                                class_name="text-xs text-gray-600 px-4 py-2.5",
                            ),
                            class_name="border-b border-gray-100 hover:bg-blue-50/30",
                        ),
                    ),
                ),
                class_name="table-auto w-full",
            ),
            rx.el.div(
                "No source vendors recorded for this item.",
                class_name="px-4 py-8 text-sm text-gray-500 text-center",
            ),
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def lots_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("boxes", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "All Lots", class_name="text-sm font-semibold text-gray-900"
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
                            "Days",
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
                            "QC",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
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
                                class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
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
                                f"{lot['days_to_expiry']}d",
                                class_name=rx.cond(
                                    lot["days_to_expiry"] <= 30,
                                    "text-xs font-semibold text-red-700 px-4 py-2.5",
                                    rx.cond(
                                        lot["days_to_expiry"] <= 90,
                                        "text-xs font-semibold text-yellow-700 px-4 py-2.5",
                                        "text-xs text-gray-600 px-4 py-2.5",
                                    ),
                                ),
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
            rx.el.div(
                "No lots associated with this item.",
                class_name="px-4 py-8 text-sm text-gray-500 text-center",
            ),
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def stock_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("layers", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Stock Balances by Lot + Location",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.cond(
            InventoryState.selected_item_balances.length() > 0,
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Lot",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Location",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Quantity",
                            class_name="text-right text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Expiry",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "QC",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        InventoryState.selected_item_balances,
                        lambda b: rx.el.tr(
                            rx.el.td(
                                b["lot_number"],
                                class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                b["location"],
                                class_name="text-sm text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                f"{b['quantity']} {b['unit']}",
                                class_name="text-sm font-semibold text-blue-700 px-4 py-2.5 text-right tabular-nums",
                            ),
                            rx.el.td(
                                b["expiry_date"],
                                class_name="text-xs text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.td(
                                status_badge(b["status"]),
                                class_name="px-4 py-2.5",
                            ),
                            class_name="border-b border-gray-100 hover:bg-blue-50/30 last:border-b-0",
                        ),
                    ),
                ),
                class_name="table-auto w-full",
            ),
            rx.el.div(
                "No stock balances available.",
                class_name="px-4 py-8 text-sm text-gray-500 text-center",
            ),
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def documents_tab() -> rx.Component:
    item = InventoryState.selected_item
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Linked Documents",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(
                GovernanceState.documents,
                lambda d: rx.cond(
                    d["linked_to"].contains(item["id"])
                    | d["linked_to"].contains(InventoryState.selected_item_id),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "file-text",
                                class_name="h-4 w-4 text-gray-500",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    d["title"],
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                rx.el.div(
                                    f"{d['doc_no']} • {d['file_name']}",
                                    class_name="text-xs text-gray-500",
                                ),
                            ),
                            class_name="flex items-center gap-3 flex-1",
                        ),
                        rx.el.span(
                            d["category"],
                            class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                        ),
                        class_name="flex items-center justify-between px-4 py-3 border-b border-gray-100 last:border-b-0",
                    ),
                    rx.fragment(),
                ),
            ),
            class_name="",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def activity_tab() -> rx.Component:
    item_id = InventoryState.selected_item_id
    return rx.el.div(
        rx.el.div(
            rx.icon("activity", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Transaction Activity",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(
                OperationsState.audit_log,
                lambda e: rx.cond(
                    e["target"].contains(item_id),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                e["action"],
                                class_name="text-[10px] font-bold px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                            ),
                            rx.el.span(
                                e["target"],
                                class_name="text-xs font-mono text-gray-700",
                            ),
                            rx.el.span(
                                e["timestamp"],
                                class_name="text-xs text-gray-500 ml-auto",
                            ),
                            class_name="flex items-center gap-2 mb-1",
                        ),
                        rx.el.div(
                            e["detail"], class_name="text-sm text-gray-700"
                        ),
                        rx.el.div(
                            rx.icon("user", class_name="h-3 w-3 text-gray-400"),
                            rx.el.span(
                                f"{e['user']} ({e['role']})",
                                class_name="text-[10px] text-gray-500",
                            ),
                            class_name="flex items-center gap-1 mt-1",
                        ),
                        class_name="px-4 py-3 border-b border-gray-100 last:border-b-0",
                    ),
                    rx.fragment(),
                ),
            ),
            class_name="max-h-96 overflow-y-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
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
                class_name="bg-white border border-gray-200 rounded-lg p-5",
            ),
            rx.el.div(
                rx.el.div(
                    tab_button("Overview", "overview", "info"),
                    tab_button("Sources", "sources", "truck"),
                    tab_button("Lots", "lots", "boxes"),
                    tab_button("Stock", "stock", "layers"),
                    tab_button("Documents", "documents", "file-text"),
                    tab_button("Activity", "activity", "activity"),
                    class_name="flex items-center border-b border-gray-200 bg-white rounded-t-lg",
                ),
                rx.el.div(
                    rx.match(
                        InventoryState.detail_tab,
                        ("overview", overview_tab()),
                        ("sources", sources_tab()),
                        ("lots", lots_tab()),
                        ("stock", stock_tab()),
                        ("documents", documents_tab()),
                        ("activity", activity_tab()),
                        overview_tab(),
                    ),
                    class_name="pt-4",
                ),
                class_name="",
            ),
            class_name="flex flex-col gap-4",
        ),
    )