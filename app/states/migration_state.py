import reflex as rx
from typing import TypedDict
from datetime import datetime, date
import uuid
import csv
import io
import logging

from app.services.csv_migration_service import (
    CSV_SPECS,
    CSV_FILE_ORDER,
    validate_required_columns,
    validate_row,
    build_idempotency_key,
)
from app.services.admin_service import can_commit_migration


class MigrationRow(TypedDict):
    row_no: int
    file_name: str
    sku: str
    item_name: str
    quantity: float
    unit: str
    expiry: str
    location: str
    lot_number: str
    status: str
    error: str
    raw: str
    idempotency_key: str
    duplicate: bool


class MigrationBatch(TypedDict):
    id: str
    batch_no: str
    file_name: str
    rows_total: int
    rows_valid: int
    rows_invalid: int
    rows_imported: int
    rows_skipped: int
    submitted_by: str
    submitted_at: str
    status: str


class CSVFileSpec(TypedDict):
    file_name: str
    label: str
    description: str
    required_columns: list[str]
    optional_columns: list[str]


MIGRATION_LOT_PREFIX = "MIG"
MIGRATION_LOCATION = "MIGRATION / UNASSIGNED"
MIGRATION_STATUS = "Released"


class MigrationState(rx.State):
    pending_rows: list[MigrationRow] = []
    batches: list[MigrationBatch] = [
        {
            "id": "MIG-001",
            "batch_no": "MIG-2024-0001",
            "file_name": "opening_balances.csv",
            "rows_total": 10,
            "rows_valid": 10,
            "rows_invalid": 0,
            "rows_imported": 10,
            "rows_skipped": 0,
            "submitted_by": "Admin",
            "submitted_at": "2024-04-01 09:00",
            "status": "Imported",
        },
    ]
    last_uploaded_file: str = ""
    last_message: str = ""
    selected_csv_type: str = "opening_balances.csv"
    imported_keys: list[str] = []

    @rx.var
    def csv_specs(self) -> list[CSVFileSpec]:
        out: list[CSVFileSpec] = []
        for fn in CSV_FILE_ORDER:
            spec = CSV_SPECS[fn]
            out.append(
                {
                    "file_name": fn,
                    "label": spec["label"],
                    "description": spec["description"],
                    "required_columns": spec["required_columns"],
                    "optional_columns": spec.get("optional_columns", []),
                }
            )
        return out

    @rx.var
    def selected_spec(self) -> CSVFileSpec:
        spec = CSV_SPECS.get(
            self.selected_csv_type, CSV_SPECS["opening_balances.csv"]
        )
        return {
            "file_name": self.selected_csv_type,
            "label": spec["label"],
            "description": spec["description"],
            "required_columns": spec["required_columns"],
            "optional_columns": spec.get("optional_columns", []),
        }

    @rx.var
    def valid_row_count(self) -> int:
        """Rows that are non-duplicate AND have no validation errors."""
        return len(
            [
                r
                for r in self.pending_rows
                if r["error"] == "" and not r["duplicate"]
            ]
        )

    @rx.var
    def invalid_row_count(self) -> int:
        """Rows with validation errors (excluding pure duplicate flags)."""
        return len(
            [
                r
                for r in self.pending_rows
                if r["error"] != "" and not r["duplicate"]
            ]
        )

    @rx.var
    def duplicate_row_count(self) -> int:
        """Rows flagged as duplicates within batch or against prior batches."""
        return len([r for r in self.pending_rows if r["duplicate"]])

    @rx.var
    def has_pending(self) -> bool:
        return len(self.pending_rows) > 0

    @rx.var
    def is_opening_balances(self) -> bool:
        return self.selected_csv_type == "opening_balances.csv"

    @rx.event
    def set_csv_type(self, t: str):
        self.selected_csv_type = t
        self.pending_rows = []
        self.last_uploaded_file = ""
        self.last_message = ""

    @rx.event
    async def handle_csv_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        file = files[0]
        try:
            data = await file.read()
            text = data.decode("utf-8", errors="replace")
            for update in self.parse_text_data(text, file.name):
                yield update
        except Exception as e:
            logging.exception(f"Error parsing migration CSV: {e}")
            yield rx.toast.error(f"Failed to parse CSV: {e}")

    @rx.event
    def parse_text_data(self, text: str, file_name: str):
        from app.states.inventory_state import InventoryState

        reader = csv.DictReader(io.StringIO(text))
        header = reader.fieldnames or []
        ok, msg = validate_required_columns(self.selected_csv_type, header)
        if not ok:
            yield rx.toast.error(f"{self.selected_csv_type}: {msg}")
            return

        # First pass: read all raw rows and compute idempotency keys so we can
        # flag EVERY occurrence of a duplicated key (not just the later ones).
        raw_rows: list[dict] = []
        for raw in reader:
            raw_rows.append(dict(raw))

        key_counts: dict[str, int] = {}
        for raw in raw_rows:
            k = build_idempotency_key(self.selected_csv_type, raw)
            key_counts[k] = key_counts.get(k, 0) + 1

        rows: list[MigrationRow] = []
        for idx, raw in enumerate(raw_rows, start=1):
            errs = validate_row(self.selected_csv_type, raw, idx)
            key = build_idempotency_key(self.selected_csv_type, raw)
            duplicate_in_batch = key_counts.get(key, 0) > 1
            duplicate_already = key in self.imported_keys
            sku = (
                raw.get("sku") or raw.get("code") or raw.get("item_sku") or ""
            ).strip()
            qty_raw = (raw.get("quantity") or "0").strip()
            try:
                qty_val = float(qty_raw) if qty_raw else 0.0
            except ValueError:
                qty_val = 0.0
            expiry = (raw.get("expiry") or "").strip()
            location = (raw.get("location") or "").strip() or MIGRATION_LOCATION
            lot = (raw.get("lot_number") or "").strip()
            item_name = (raw.get("name") or "").strip()
            unit = (raw.get("unit") or "").strip()
            if self.selected_csv_type == "opening_balances.csv":
                if not lot:
                    lot = f"{MIGRATION_LOT_PREFIX}-{sku or 'ITEM'}-{idx:03d}"
                elif not lot.startswith(f"{MIGRATION_LOT_PREFIX}-"):
                    lot = f"{MIGRATION_LOT_PREFIX}-{lot}"
            is_duplicate = duplicate_in_batch or duplicate_already
            err_str = ""
            if errs:
                err_str = "; ".join(errs)
            elif duplicate_in_batch:
                err_str = (
                    "Duplicate idempotency key within this file "
                    "(all occurrences flagged)"
                )
            elif duplicate_already:
                err_str = "Already imported in a previous batch"
            rows.append(
                {
                    "row_no": idx,
                    "file_name": self.selected_csv_type,
                    "sku": sku,
                    "item_name": item_name,
                    "quantity": qty_val,
                    "unit": unit,
                    "expiry": expiry or "—",
                    "location": location,
                    "lot_number": lot,
                    "status": MIGRATION_STATUS,
                    "error": err_str,
                    "raw": str({k: v for k, v in raw.items()})[:160],
                    "idempotency_key": key,
                    "duplicate": is_duplicate,
                }
            )
        self.pending_rows = rows
        self.last_uploaded_file = file_name
        self.last_message = (
            f"Dry-run parsed {len(rows)} rows from {file_name} "
            f"({self.selected_csv_type})"
        )
        yield rx.toast.success(self.last_message)

    @rx.event
    def load_sample_csv(self):
        if self.selected_csv_type == "opening_balances.csv":
            sample_text = (
                "sku,quantity,expiry,location,lot_number\n"
                "RGT-MTH-001,10.0,2026-08-01,Migration Holding Area,MIG-RGT-MTH-001-001\n"
                "STD-PAR-003,1.5,2025-05-15,Migration Holding Area,MIG-STD-PAR-003-002\n"
                ",-5.0,2024-12-31,Migration Holding Area,MIG-INVALID-003\n"
                "RGT-MTH-001,10.0,2026-08-01,Migration Holding Area,MIG-RGT-MTH-001-001\n"
                "RGT-MTH-001,10.0,2026-08-01,Migration Holding Area,MIG-RGT-MTH-001-001\n"
            )
        elif self.selected_csv_type == "categories.csv":
            sample_text = (
                "code,name,description\n"
                "SOLV,Solvent,Organic and aqueous solvents\n"
                "RGT,Reagent,General laboratory reagents\n"
                "STD,Reference Standard,USP/EP/in-house standards\n"
            )
        elif self.selected_csv_type == "vendors.csv":
            sample_text = (
                "code,name,category,contact_person,email,phone\n"
                "VEN-MRK,Merck KGaA,Reagent Manufacturer,Hans Mueller,h.mueller@merck.de,+49 6151 720\n"
                "VEN-SIG,Sigma-Aldrich,Reagent Manufacturer,Maria Lopez,m.lopez@sigmaaldrich.com,+1 314 771 5765\n"
            )
        elif self.selected_csv_type == "items.csv":
            sample_text = (
                "sku,name,category,unit,legacy_code,min_level,max_level,is_napza,is_hazard\n"
                "RGT-MTH-001,Methanol HPLC Grade,Solvent,L,QC-MTH-OLD-01,20.0,100.0,false,true\n"
                "STD-PAR-003,Paracetamol Reference Standard,Reference Standard,g,QC-PAR-OLD-03,2.0,10.0,false,false\n"
            )
        elif self.selected_csv_type == "locations.csv":
            sample_text = (
                "code,name,description,restricted\n"
                "SOLV-A,Solvent Cabinet A,Vented flammable cabinet,false\n"
                "VLT-NPZ,Vault NPZ-01,Restricted NAPZA vault,true\n"
            )
        else:
            spec = CSV_SPECS[self.selected_csv_type]
            cols = spec["required_columns"] + spec.get("optional_columns", [])
            sample_text = (
                ",".join(cols) + "\n" + ",".join(["sample"] * len(cols)) + "\n"
            )

        for update in self.parse_text_data(
            sample_text, f"sample_{self.selected_csv_type}"
        ):
            yield update

    @rx.event
    def clear_pending(self):
        self.pending_rows = []
        self.last_uploaded_file = ""
        self.last_message = ""

    @rx.event
    async def commit_migration(self):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState
        from app.states.operations_state import OperationsState

        auth = await self.get_state(AuthState)
        ok, reason = can_commit_migration(auth.current_role)
        if not ok:
            yield rx.toast.error(reason)
            return

        if not self.pending_rows:
            yield rx.toast.error("No rows to import.")
            return

        valid_rows = [
            r
            for r in self.pending_rows
            if r["error"] == "" and not r["duplicate"]
        ]
        skipped = len(self.pending_rows) - len(valid_rows)

        if not valid_rows:
            yield rx.toast.error("No valid rows to import.")
            return

        if self.selected_csv_type != "opening_balances.csv":
            for r in valid_rows:
                self.imported_keys.append(r["idempotency_key"])
            new_batch: MigrationBatch = {
                "id": f"MIG-{uuid.uuid4().hex[:6].upper()}",
                "batch_no": f"MIG-2024-{1 + len(self.batches):04d}",
                "file_name": self.last_uploaded_file or self.selected_csv_type,
                "rows_total": len(self.pending_rows),
                "rows_valid": len(valid_rows),
                "rows_invalid": self.invalid_row_count,
                "rows_imported": len(valid_rows),
                "rows_skipped": skipped,
                "submitted_by": auth.current_user,
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "Imported (Scaffold)",
            }
            self.batches.insert(0, new_batch)
            self.pending_rows = []
            self.last_uploaded_file = ""
            self.last_message = f"Imported {len(valid_rows)} {self.selected_csv_type} rows (master-data scaffold)"
            yield rx.toast.success(self.last_message)
            return

        inv = await self.get_state(InventoryState)
        ops = await self.get_state(OperationsState)

        imported = 0
        for r in valid_rows:
            target = next((i for i in inv.items if i["sku"] == r["sku"]), None)
            if target is None:
                continue
            if r["quantity"] < 0:
                continue
            target["on_hand"] = round(target["on_hand"] + r["quantity"], 4)
            target["available"] = round(target["available"] + r["quantity"], 4)
            target["total_received"] = round(
                target["total_received"] + r["quantity"], 4
            )
            target["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            if target["on_hand"] > 0 and target["status"] == "Out of Stock":
                target["status"] = "Released"

            try:
                if r["expiry"] not in ("", "—", "-", "None", "none"):
                    yyyy, mm, dd = r["expiry"].split("-")
                    days = (
                        date(int(yyyy), int(mm), int(dd)) - date.today()
                    ).days
                    expiry_known = True
                    expiry_value = r["expiry"]
                else:
                    days = 10**9
                    expiry_known = False
                    expiry_value = None
            except Exception:
                logging.exception("Migration expiry parse error")
                days = 10**9
                expiry_known = False
                expiry_value = None

            inv.lots.insert(
                0,
                {
                    "id": f"LOT-{uuid.uuid4().hex[:6].upper()}",
                    "item_id": target["id"],
                    "item_name": target["name"],
                    "lot_number": r["lot_number"],
                    "quantity": r["quantity"],
                    "unit": r["unit"] or target["unit"],
                    "received_date": datetime.now().strftime("%Y-%m-%d"),
                    "expiry_date": expiry_value,
                    "expiry_known": expiry_known,
                    "status": MIGRATION_STATUS,
                    "location": r["location"],
                    "vendor": "Migration",
                    "days_to_expiry": days,
                },
            )
            ops._audit(
                auth.current_user,
                auth.current_role,
                "OPENING_BALANCE",
                f"{target['id']} / {r['lot_number']}",
                f"Migrated {r['quantity']} {target['unit']} → {r['location']} (Released)",
            )
            self.imported_keys.append(r["idempotency_key"])
            imported += 1

        new_batch: MigrationBatch = {
            "id": f"MIG-{uuid.uuid4().hex[:6].upper()}",
            "batch_no": f"MIG-2024-{1 + len(self.batches):04d}",
            "file_name": self.last_uploaded_file or "manual_entry",
            "rows_total": len(self.pending_rows),
            "rows_valid": len(valid_rows),
            "rows_invalid": self.invalid_row_count,
            "rows_imported": imported,
            "rows_skipped": skipped,
            "submitted_by": auth.current_user,
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Imported",
        }
        self.batches.insert(0, new_batch)
        self.pending_rows = []
        self.last_uploaded_file = ""
        self.last_message = f"Imported {imported} opening balances"
        yield rx.toast.success(self.last_message)