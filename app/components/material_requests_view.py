import reflex as rx
from app.states.operations_state import OperationsState
from app.components.badges import status_badge, hazard_badge


def request_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("clipboard-list", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "New Material Request",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-4 py-3 border-b border-gray-200",
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
                        value=OperationsState.mr_item_id,
                        on_change=OperationsState.set_mr_item,
                        class_name="appearance-none w-full pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-700 focus:outline-none focus:border-blue-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.label(
                    "Quantity",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="0.00",
                    default_value=OperationsState.mr_quantity,
                    on_change=OperationsState.set_mr_quantity.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Priority",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Low", value="Low"),
                        rx.el.option("Normal", value="Normal"),
                        rx.el.option("High", value="High"),
                        value=OperationsState.mr_priority,
                        on_change=OperationsState.set_mr_priority,
                        class_name="appearance-none w-full pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-700 focus:outline-none focus:border-blue-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Purpose",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Test/method purpose",
                    default_value=OperationsState.mr_purpose,
                    on_change=OperationsState.set_mr_purpose.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.label(
                    "Notes",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.textarea(
                    placeholder="Optional details, references, or batch numbers…",
                    default_value=OperationsState.mr_notes,
                    on_change=OperationsState.set_mr_notes.debounce(300),
                    rows="2",
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
                class_name="col-span-2",
            ),
            class_name="grid grid-cols-2 gap-3 px-4 py-4",
        ),
        rx.cond(
            OperationsState.mr_item_id != "",
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "info", class_name="h-4 w-4 text-blue-500 shrink-0"
                    ),
                    rx.el.div(
                        rx.el.div(
                            OperationsState.selected_mr_item["name"],
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            f"Available: {OperationsState.selected_mr_item['available']} {OperationsState.selected_mr_item['unit']}",
                            class_name="text-xs text-gray-600",
                        ),
                    ),
                    rx.el.div(
                        hazard_badge(
                            OperationsState.selected_mr_item["is_hazard"],
                            OperationsState.selected_mr_item["is_napza"],
                        ),
                        class_name="ml-auto",
                    ),
                    class_name="flex items-center gap-3 px-4 py-2.5",
                ),
                rx.cond(
                    OperationsState.selected_mr_item["is_napza"],
                    rx.el.div(
                        rx.icon(
                            "shield-alert",
                            class_name="h-4 w-4 text-purple-600 shrink-0",
                        ),
                        rx.el.span(
                            "NAPZA controlled substance — registry approval and dual sign-off required.",
                            class_name="text-xs text-purple-800",
                        ),
                        class_name="flex items-center gap-2 mx-4 mb-2 px-3 py-2 bg-purple-50 border border-purple-200 rounded-md",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    OperationsState.selected_mr_item["is_hazard"]
                    & ~OperationsState.selected_mr_item["is_napza"],
                    rx.el.div(
                        rx.icon(
                            "triangle-alert",
                            class_name="h-4 w-4 text-orange-600 shrink-0",
                        ),
                        rx.el.span(
                            "Hazardous material — confirm PPE, fume hood, and SDS reference before use.",
                            class_name="text-xs text-orange-800",
                        ),
                        class_name="flex items-center gap-2 mx-4 mb-2 px-3 py-2 bg-orange-50 border border-orange-200 rounded-md",
                    ),
                    rx.fragment(),
                ),
                class_name="bg-gray-50 border-t border-gray-100",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("send", class_name="h-4 w-4"),
                "Submit Request",
                on_click=OperationsState.submit_material_request,
                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
            ),
            class_name="px-4 py-3 border-t border-gray-200 flex justify-end",
        ),
        class_name="bg-white border border-gray-200 rounded-lg",
    )


def filter_chip(label: str, value: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: OperationsState.set_request_filter(value),
        class_name=rx.cond(
            OperationsState.request_status_filter == value,
            "px-3 py-1.5 text-xs font-medium rounded-md bg-blue-600 text-white",
            "px-3 py-1.5 text-xs font-medium rounded-md bg-white text-gray-700 border border-gray-200 hover:bg-gray-50",
        ),
    )


def request_row(req: rx.Var) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            req["request_no"],
            class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
        ),
        rx.el.td(
            req["requester"], class_name="text-sm text-gray-700 px-4 py-2.5"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    req["item_name"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.div(
                    req["item_sku"],
                    class_name="text-[10px] font-mono text-gray-500",
                ),
            ),
            class_name="px-4 py-2.5",
        ),
        rx.el.td(
            f"{req['quantity']} {req['unit']}",
            class_name="text-sm text-gray-900 px-4 py-2.5 tabular-nums",
        ),
        rx.el.td(
            req["purpose"],
            class_name="text-xs text-gray-600 px-4 py-2.5 max-w-xs truncate",
        ),
        rx.el.td(
            hazard_badge(req["is_hazard"], req["is_napza"]),
            class_name="px-4 py-2.5",
        ),
        rx.el.td(
            rx.el.span(
                req["priority"],
                class_name=rx.match(
                    req["priority"],
                    (
                        "High",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200 w-fit",
                    ),
                    (
                        "Normal",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                    ),
                    (
                        "Low",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
                    ),
                    "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
                ),
            ),
            class_name="px-4 py-2.5",
        ),
        rx.el.td(
            rx.el.span(
                req["status"],
                class_name=rx.match(
                    req["status"],
                    (
                        "Approved",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200 w-fit",
                    ),
                    (
                        "Pending Approval",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
                    ),
                    (
                        "Issued",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                    ),
                    (
                        "Rejected",
                        "px-2 py-0.5 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200 w-fit",
                    ),
                    "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
                ),
            ),
            class_name="px-4 py-2.5",
        ),
        rx.el.td(
            req["created_at"], class_name="text-xs text-gray-500 px-4 py-2.5"
        ),
        rx.el.td(
            rx.cond(
                req["status"] == "Pending Approval",
                rx.el.div(
                    rx.el.button(
                        rx.icon("check", class_name="h-3.5 w-3.5"),
                        on_click=lambda: OperationsState.approve_request(
                            req["id"]
                        ),
                        class_name="p-1.5 rounded-md text-green-600 hover:bg-green-50",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-3.5 w-3.5"),
                        on_click=lambda: OperationsState.reject_request(
                            req["id"]
                        ),
                        class_name="p-1.5 rounded-md text-red-600 hover:bg-red-50",
                    ),
                    class_name="flex items-center gap-1",
                ),
                rx.fragment(),
            ),
            class_name="px-4 py-2.5",
        ),
        class_name="border-b border-gray-100 hover:bg-blue-50/30",
    )


def request_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "All Requests",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    f"{OperationsState.pending_request_count} pending",
                    class_name="text-[10px] font-semibold px-2 py-0.5 ml-2 rounded bg-yellow-50 text-yellow-700 border border-yellow-200",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                filter_chip("All", "All"),
                filter_chip("Pending", "Pending Approval"),
                filter_chip("Approved", "Approved"),
                filter_chip("Issued", "Issued"),
                filter_chip("Rejected", "Rejected"),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex items-center justify-between px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Request #",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Requester",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Item",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Qty",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Purpose",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Flags",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Priority",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Created",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th("", class_name="px-4 py-2.5"),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(OperationsState.filtered_requests, request_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def material_requests_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            request_form(),
            class_name="grid grid-cols-1 gap-4",
        ),
        request_table(),
    )