import reflex as rx
from app.states.migration_state import MigrationState
from app.states.auth_state import AuthState

UPLOAD_ID = "migration_csv"


def file_chip(spec) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                spec["file_name"],
                class_name="text-[11px] font-mono font-semibold",
            ),
            rx.el.div(spec["label"], class_name="text-xs"),
            class_name="flex flex-col items-start",
        ),
        on_click=lambda: MigrationState.set_csv_type(spec["file_name"]),
        class_name=rx.cond(
            MigrationState.selected_csv_type == spec["file_name"],
            "px-3 py-2 rounded-md border-2 border-blue-500 bg-blue-50 text-blue-700 text-left",
            "px-3 py-2 rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 text-left",
        ),
    )


def file_selector_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("files", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                "11 Required Access CSV Files",
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.span(
                "Select a file type, then upload to dry-run",
                class_name="text-xs text-gray-500 ml-2",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(MigrationState.csv_specs, file_chip),
            class_name="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 p-4",
        ),
        class_name="bg-white border border-gray-200 rounded-lg",
    )


def required_col_chips() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            "Required columns",
            class_name="text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1",
        ),
        rx.el.div(
            rx.foreach(
                MigrationState.selected_spec["required_columns"],
                lambda c: rx.el.span(
                    c,
                    class_name="inline-block text-[11px] font-mono px-1.5 py-0.5 mr-1 mb-1 rounded bg-blue-50 text-blue-700 border border-blue-200",
                ),
            ),
            class_name="flex flex-wrap",
        ),
        rx.el.div(
            "Optional columns",
            class_name="text-[10px] font-semibold text-gray-500 uppercase tracking-wide mt-2 mb-1",
        ),
        rx.el.div(
            rx.foreach(
                MigrationState.selected_spec["optional_columns"],
                lambda c: rx.el.span(
                    c,
                    class_name="inline-block text-[11px] font-mono px-1.5 py-0.5 mr-1 mb-1 rounded bg-gray-50 text-gray-600 border border-gray-200",
                ),
            ),
            class_name="flex flex-wrap",
        ),
        class_name="px-4 py-3 border-t border-gray-100 bg-gray-50",
    )


def upload_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("database", class_name="h-4 w-4 text-blue-500"),
            rx.el.span(
                MigrationState.selected_spec["label"],
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.span(
                MigrationState.selected_spec["file_name"],
                class_name="text-[11px] font-mono px-2 py-0.5 ml-2 rounded bg-gray-100 text-gray-700 border border-gray-200",
            ),
            class_name="flex items-center gap-2 px-4 py-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                MigrationState.selected_spec["description"],
                class_name="text-xs text-gray-600 mb-3",
            ),
            rx.el.div(
                rx.icon("info", class_name="h-3.5 w-3.5 text-blue-500"),
                rx.el.span(
                    "Dry-run only. Validation runs row-by-row with idempotency keys to prevent duplicate imports across batches.",
                    class_name="text-xs text-blue-700",
                ),
                class_name="flex items-center gap-1.5 px-3 py-2 bg-blue-50 border border-blue-200 rounded-md mb-3",
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
                        "Validation only — no database writes until commit",
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
        ),
        required_col_chips(),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )


def preview_table() -> rx.Component:
    return rx.cond(
        MigrationState.has_pending,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"Dry-run preview: {MigrationState.last_uploaded_file}",
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
                    rx.el.span(
                        f"{MigrationState.duplicate_row_count} duplicates",
                        class_name="text-[10px] font-semibold px-2 py-0.5 ml-1 rounded bg-yellow-50 text-yellow-700 border border-yellow-200",
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
                rx.el.div(
                    rx.icon("info", class_name="h-3.5 w-3.5 text-blue-500"),
                    rx.el.span(
                        "Re-importing the same file is safe: rows already imported (matching idempotency keys) are flagged as duplicates and skipped on commit.",
                        class_name="text-xs text-blue-700",
                    ),
                    class_name="flex items-center gap-1.5 mx-4 my-3 px-3 py-2 bg-blue-50 border border-blue-200 rounded-md",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Row",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "File",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Key Field",
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
                                "Idempotency Key",
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
                                    r["file_name"],
                                    class_name="text-[11px] font-mono text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    r["sku"],
                                    class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
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
                                    r["idempotency_key"],
                                    class_name="text-[10px] font-mono text-gray-500 px-4 py-2.5 truncate max-w-[180px]",
                                ),
                                rx.el.td(
                                    rx.cond(
                                        r["error"] != "",
                                        rx.el.span(
                                            r["error"],
                                            class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-red-50 text-red-700 border border-red-200 w-fit",
                                        ),
                                        rx.cond(
                                            r["duplicate"],
                                            rx.el.span(
                                                "Duplicate",
                                                class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
                                            ),
                                            rx.el.span(
                                                "Valid",
                                                class_name="text-[10px] font-medium px-2 py-0.5 rounded bg-green-50 text-green-700 border border-green-200 w-fit",
                                            ),
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                class_name=rx.cond(
                                    r["error"] != "",
                                    "border-b border-gray-100 bg-red-50/30",
                                    rx.cond(
                                        r["duplicate"],
                                        "border-b border-gray-100 bg-yellow-50/30",
                                        "border-b border-gray-100 hover:bg-blue-50/30",
                                    ),
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
    )


def batches_table() -> rx.Component:
    return rx.el.div(
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
                            "Skipped",
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
                                b["rows_skipped"].to_string(),
                                class_name="text-sm text-yellow-700 px-4 py-2.5 tabular-nums",
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
    )


def admin_banner() -> rx.Component:
    return rx.cond(
        AuthState.current_role != "Admin",
        rx.el.div(
            rx.icon("lock", class_name="h-4 w-4 text-orange-600"),
            rx.el.span(
                f"Current role ({AuthState.current_role}) can preview and validate, but only Admin can commit migration batches.",
                class_name="text-xs text-orange-700",
            ),
            class_name="flex items-center gap-2 px-3 py-2 bg-orange-50 border border-orange-200 rounded-md",
        ),
        rx.el.div(
            rx.icon("shield-check", class_name="h-4 w-4 text-green-600"),
            rx.el.span(
                "Signed in as Admin — commit is enabled for valid, non-duplicate rows.",
                class_name="text-xs text-green-700",
            ),
            class_name="flex items-center gap-2 px-3 py-2 bg-green-50 border border-green-200 rounded-md",
        ),
    )


def migration_view() -> rx.Component:
    return rx.fragment(
        admin_banner(),
        file_selector_card(),
        upload_card(),
        preview_table(),
        batches_table(),
    )