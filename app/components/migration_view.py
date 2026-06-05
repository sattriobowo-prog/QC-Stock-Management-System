import reflex as rx
from app.states.migration_state import MigrationState
from app.states.auth_state import AuthState

UPLOAD_ID = "migration_csv"


def migration_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.icon("database", class_name="h-4 w-4 text-blue-500"),
                rx.el.span(
                    "Opening Balance Migration",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("info", class_name="h-3.5 w-3.5 text-blue-500"),
                    rx.el.span(
                        "All migrated lots are tagged with the MIG prefix, placed in the Migration Holding Area, and posted as Released opening-balance transactions.",
                        class_name="text-xs text-blue-700",
                    ),
                    class_name="flex items-center gap-1.5 px-3 py-2 bg-blue-50 border border-blue-200 rounded-md mb-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            "Required CSV columns",
                            class_name="text-xs font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.div(
                            rx.el.code(
                                "sku, quantity, expiry, location, lot_number"
                            ),
                            class_name="text-[11px] font-mono text-gray-700 bg-gray-50 px-2 py-1 rounded border border-gray-200",
                        ),
                        class_name="mb-3",
                    ),
                    rx.upload.root(
                        rx.el.div(
                            rx.icon(
                                "cloud-upload",
                                class_name="h-10 w-10 text-gray-400 mb-2",
                            ),
                            rx.el.div(
                                "Drop CSV file or click to upload",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                "Supports .csv files up to 5 MB",
                                class_name="text-xs text-gray-500 mt-1",
                            ),
                            class_name="flex flex-col items-center justify-center py-8 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50",
                        ),
                        id=UPLOAD_ID,
                        accept={"text/csv": [".csv"]},
                        max_files=1,
                        on_drop=MigrationState.handle_csv_upload(
                            rx.upload_files(upload_id=UPLOAD_ID)
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("file-text", class_name="h-4 w-4"),
                            "Load Sample Preview",
                            on_click=MigrationState.load_sample_csv,
                            class_name="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 rounded-lg",
                        ),
                        class_name="flex items-center justify-end mt-3",
                    ),
                    class_name="",
                ),
                class_name="px-4 py-4",
            ),
            class_name="bg-white border border-gray-200 rounded-lg",
        ),
        rx.cond(
            MigrationState.has_pending,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            f"Preview: {MigrationState.last_uploaded_file}",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.span(
                            f"{MigrationState.valid_row_count} valid",
                            class_name="text-[10px] font-semibold px-2 py-0.5 ml-2 rounded bg-green-50 text-green-700 border border-green-200",
                        ),
                        rx.el.span(
                            f"{MigrationState.invalid_row_count} errors",
                            class_name="text-[10px] font-semibold px-2 py-0.5 ml-1 rounded bg-red-50 text-red-700 border border-red-200",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Clear",
                            on_click=MigrationState.clear_pending,
                            class_name="px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 rounded-md",
                        ),
                        rx.cond(
                            AuthState.current_role == "Admin",
                            rx.el.button(
                                rx.icon("check", class_name="h-3.5 w-3.5"),
                                "Commit Import",
                                on_click=MigrationState.commit_migration,
                                class_name="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md",
                            ),
                            rx.el.span(
                                "Admin role required to commit",
                                class_name="text-[10px] text-gray-500 italic",
                            ),
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    class_name="flex items-center justify-between px-4 py-3 border-b border-gray-200",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "#",
                                    class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.th(
                                    "SKU",
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
                                    "Expiry",
                                    class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.th(
                                    "Lot",
                                    class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.th(
                                    "Location",
                                    class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.th(
                                    "Validation",
                                    class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                                ),
                                class_name="bg-gray-50 border-b border-gray-200",
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                MigrationState.pending_rows,
                                lambda r: rx.el.tr(
                                    rx.el.td(
                                        r["row_no"].to_string(),
                                        class_name="text-xs text-gray-600 px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        r["sku"],
                                        class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        r["item_name"],
                                        class_name="text-sm text-gray-900 px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        f"{r['quantity']} {r['unit']}",
                                        class_name="text-sm text-gray-900 px-4 py-2.5 tabular-nums",
                                    ),
                                    rx.el.td(
                                        r["expiry"],
                                        class_name="text-xs text-gray-600 px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        r["lot_number"],
                                        class_name="text-xs font-mono text-blue-700 px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        r["location"],
                                        class_name="text-xs text-gray-600 px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            r["status"],
                                            class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-green-50 text-green-700 border border-green-200 w-fit",
                                        ),
                                        class_name="px-4 py-2.5",
                                    ),
                                    rx.el.td(
                                        rx.cond(
                                            r["error"] != "",
                                            rx.el.span(
                                                r["error"],
                                                class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-red-50 text-red-700 border border-red-200 w-fit",
                                            ),
                                            rx.el.span(
                                                "Valid",
                                                class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-green-50 text-green-700 border border-green-200 w-fit",
                                            ),
                                        ),
                                        class_name="px-4 py-2.5",
                                    ),
                                    class_name=rx.cond(
                                        r["error"] != "",
                                        "border-b border-gray-100 bg-red-50/30",
                                        "border-b border-gray-100 hover:bg-blue-50/30",
                                    ),
                                ),
                            ),
                        ),
                        class_name="table-auto w-full",
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Migration Batches",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Batch #",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "File",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Total",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Valid",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Invalid",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Imported",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Submitted",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            class_name="bg-gray-50 border-b border-gray-200",
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            MigrationState.batches,
                            lambda b: rx.el.tr(
                                rx.el.td(
                                    b["batch_no"],
                                    class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    b["file_name"],
                                    class_name="text-xs text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    b["rows_total"].to_string(),
                                    class_name="text-sm text-gray-900 px-4 py-2.5 tabular-nums",
                                ),
                                rx.el.td(
                                    b["rows_valid"].to_string(),
                                    class_name="text-sm text-green-700 px-4 py-2.5 tabular-nums",
                                ),
                                rx.el.td(
                                    b["rows_invalid"].to_string(),
                                    class_name="text-sm text-red-700 px-4 py-2.5 tabular-nums",
                                ),
                                rx.el.td(
                                    b["rows_imported"].to_string(),
                                    class_name="text-sm text-blue-700 px-4 py-2.5 tabular-nums",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.div(
                                            b["submitted_by"],
                                            class_name="text-sm text-gray-700",
                                        ),
                                        rx.el.div(
                                            b["submitted_at"],
                                            class_name="text-xs text-gray-500",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        b["status"],
                                        class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-green-50 text-green-700 border border-green-200 w-fit",
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
        ),
    )