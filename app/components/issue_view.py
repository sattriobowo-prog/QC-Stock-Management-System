import reflex as rx
from app.states.operations_state import OperationsState
from app.components.badges import hazard_badge


def fefo_lot_row(lot: rx.Var, idx: rx.Var[int]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.cond(
                idx == 0,
                rx.el.span(
                    "FEFO",
                    class_name="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                ),
                rx.fragment(),
            ),
            class_name="px-3 py-2",
        ),
        rx.el.td(
            lot["lot_number"],
            class_name="text-xs font-mono text-gray-700 px-3 py-2",
        ),
        rx.el.td(
            f"{lot['quantity']} {lot['unit']}",
            class_name="text-sm text-gray-900 px-3 py-2 tabular-nums",
        ),
        rx.el.td(
            lot["expiry_date"], class_name="text-xs text-gray-600 px-3 py-2"
        ),
        rx.el.td(
            f"{lot['days_to_expiry']}d",
            class_name="text-xs text-gray-600 px-3 py-2",
        ),
        rx.el.td(
            rx.el.button(
                rx.cond(
                    OperationsState.issue_lot_override == lot["lot_number"],
                    "Selected",
                    "Select",
                ),
                on_click=lambda: OperationsState.set_issue_lot_override(
                    lot["lot_number"]
                ),
                class_name=rx.cond(
                    OperationsState.issue_lot_override == lot["lot_number"],
                    "px-2 py-1 text-xs font-medium rounded-md bg-blue-600 text-white",
                    "px-2 py-1 text-xs font-medium rounded-md bg-white text-blue-700 border border-blue-200 hover:bg-blue-50",
                ),
            ),
            class_name="px-3 py-2",
        ),
        class_name="border-b border-gray-100",
    )


def issue_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("circle_minus", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Issue / Consume",
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
                        value=OperationsState.issue_item_id,
                        on_change=OperationsState.set_issue_item,
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
                    default_value=OperationsState.issue_quantity,
                    on_change=OperationsState.set_issue_quantity.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Recipient",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Analyst / lab user",
                    default_value=OperationsState.issue_recipient,
                    on_change=OperationsState.set_issue_recipient.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Purpose",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Method / test name",
                    default_value=OperationsState.issue_purpose,
                    on_change=OperationsState.set_issue_purpose.debounce(300),
                    class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-900 focus:outline-none focus:border-blue-500",
                ),
                class_name="col-span-2",
            ),
            class_name="grid grid-cols-2 gap-3 px-4 py-4",
        ),
        rx.cond(
            OperationsState.issue_item_id != "",
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            OperationsState.selected_issue_item["name"],
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            f"Available: {OperationsState.selected_issue_item['available']} {OperationsState.selected_issue_item['unit']}",
                            class_name="text-xs text-gray-600",
                        ),
                    ),
                    hazard_badge(
                        OperationsState.selected_issue_item["is_hazard"],
                        OperationsState.selected_issue_item["is_napza"],
                    ),
                    class_name="flex items-center justify-between px-4 py-2.5 bg-gray-50 border-y border-gray-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "layers", class_name="h-3.5 w-3.5 text-blue-500"
                        ),
                        rx.el.span(
                            "Eligible Lots (Released only, FEFO ordered)",
                            class_name="text-xs font-semibold text-gray-700",
                        ),
                        class_name="flex items-center gap-1.5 px-4 py-2.5 border-b border-gray-100",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-3 py-2",
                                    ),
                                    rx.el.th(
                                        "Lot",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-3 py-2",
                                    ),
                                    rx.el.th(
                                        "Qty",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-3 py-2",
                                    ),
                                    rx.el.th(
                                        "Expiry",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-3 py-2",
                                    ),
                                    rx.el.th(
                                        "To Exp.",
                                        class_name="text-left text-xs font-semibold text-gray-600 px-3 py-2",
                                    ),
                                    rx.el.th("", class_name="px-3 py-2"),
                                    class_name="bg-gray-50 border-b border-gray-200",
                                ),
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    OperationsState.fefo_lots_for_issue,
                                    lambda lot, idx: fefo_lot_row(lot, idx),
                                ),
                            ),
                            class_name="table-auto w-full",
                        ),
                        class_name="px-2",
                    ),
                    rx.cond(
                        OperationsState.issue_lot_override != "",
                        rx.el.div(
                            rx.el.label(
                                "Override Reason (required when bypassing FEFO)",
                                class_name="text-xs font-medium text-orange-700 mb-1 block",
                            ),
                            rx.el.input(
                                placeholder="Why is this lot being issued instead of the FEFO lot?",
                                default_value=OperationsState.issue_override_reason,
                                on_change=OperationsState.set_issue_override_reason.debounce(
                                    300
                                ),
                                class_name="w-full px-3 py-2 text-sm border border-orange-300 rounded-lg bg-orange-50 text-gray-900 focus:outline-none focus:border-orange-500",
                            ),
                            class_name="px-4 py-3 bg-orange-50 border-t border-orange-200",
                        ),
                        rx.fragment(),
                    ),
                ),
                class_name="",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("info", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    "Negative stock is rejected. Only Released lots are eligible.",
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.button(
                rx.icon("circle_minus", class_name="h-4 w-4"),
                "Issue Stock",
                on_click=OperationsState.submit_issue,
                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
            ),
            class_name="flex items-center justify-between px-4 py-3 border-t border-gray-200",
        ),
        class_name="bg-white border border-gray-200 rounded-lg",
    )


def issue_history_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("history", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "Recent Issue / Consume Records",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Issue #",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Item",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Lot",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Qty",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Recipient",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Purpose",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Override",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        rx.el.th(
                            "Issued At",
                            class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                        ),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        OperationsState.issues,
                        lambda iss: rx.el.tr(
                            rx.el.td(
                                iss["issue_no"],
                                class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                iss["item_name"],
                                class_name="text-sm font-medium text-gray-900 px-4 py-2.5",
                            ),
                            rx.el.td(
                                iss["lot_number"],
                                class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                f"{iss['quantity']} {iss['unit']}",
                                class_name="text-sm text-gray-900 px-4 py-2.5 tabular-nums",
                            ),
                            rx.el.td(
                                iss["issued_to"],
                                class_name="text-sm text-gray-700 px-4 py-2.5",
                            ),
                            rx.el.td(
                                iss["purpose"],
                                class_name="text-xs text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.td(
                                rx.cond(
                                    iss["override_reason"] != "",
                                    rx.el.span(
                                        iss["override_reason"],
                                        class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-orange-50 text-orange-700 border border-orange-200 w-fit",
                                    ),
                                    rx.el.span(
                                        "FEFO",
                                        class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                                    ),
                                ),
                                class_name="px-4 py-2.5",
                            ),
                            rx.el.td(
                                iss["issued_at"],
                                class_name="text-xs text-gray-500 px-4 py-2.5",
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


def issue_view() -> rx.Component:
    return rx.fragment(
        issue_form(),
        issue_history_table(),
    )