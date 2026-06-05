import reflex as rx
from app.states.governance_state import GovernanceState


def documents_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.icon("file-text", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "Document Categories",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(
                    GovernanceState.document_categories,
                    lambda c: rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                c["name"],
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.span(
                                c["required_for"],
                                class_name="text-[10px] font-medium px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                            ),
                            class_name="flex items-center justify-between mb-1",
                        ),
                        rx.el.div(
                            c["description"],
                            class_name="text-xs text-gray-600 mb-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "calendar", class_name="h-3 w-3 text-gray-400"
                            ),
                            rx.el.span(
                                f"Retention: {c['retention_days']} days",
                                class_name="text-[10px] text-gray-500",
                            ),
                            class_name="flex items-center gap-1",
                        ),
                        class_name="border border-gray-200 rounded-lg p-3 bg-white",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 p-4",
            ),
            class_name="bg-white border border-gray-200 rounded-lg",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Document Library",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Doc #",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Title",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Category",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Linked To",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Uploaded",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Expiry",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            class_name="bg-gray-50 border-b border-gray-200",
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            GovernanceState.documents,
                            lambda d: rx.el.tr(
                                rx.el.td(
                                    d["doc_no"],
                                    class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.div(
                                            d["title"],
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.div(
                                            d["file_name"],
                                            class_name="text-[10px] font-mono text-gray-500",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        d["category"],
                                        class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 w-fit",
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    d["linked_to"],
                                    class_name="text-xs font-mono text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.div(
                                            d["uploaded_by"],
                                            class_name="text-sm text-gray-700",
                                        ),
                                        rx.el.div(
                                            d["uploaded_at"],
                                            class_name="text-xs text-gray-500",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    d["expiry"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
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
        ),
    )