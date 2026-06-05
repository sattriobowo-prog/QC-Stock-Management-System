import reflex as rx
from typing import TypedDict
from datetime import datetime
import uuid
import csv
import io
import logging


class MigrationRow(TypedDict):
    row_no: int
    sku: str
    item_name: str
    quantity: float
    unit: str
    expiry: str
    location: str
    lot_number: str
    status: str
    error: str


class MigrationBatch(TypedDict):
    id: str
    batch_no: str
    file_name: str
    rows_total: int
    rows_valid: int
    rows_invalid: int
    rows_imported: int
    submitted_by: str
    submitted_at: str
    status: str


MIGRATION_LOT_PREFIX = "MIG"
MIGRATION_LOCATION = "Migration Holding Area"
MIGRATION_STATUS = "Released"


class MigrationState(rx.State):
    pending_rows: list[MigrationRow] = []
    batches: list[MigrationBatch] = [
        {
            "id": "MIG-001",
            "batch_no": "MIG-2024-0001",
            "file_name": "opening_balance_init.csv",
            "rows_total": 10,
            "rows_valid": 10,
            "rows_invalid": 0,
            "rows_imported": 10,
            "submitted_by": "Admin",
            "submitted_at": "2024-04-01 09:00",
            "status": "Imported",
        },
    ]
    last_uploaded_file: str = ""
    last_message: str = ""

    @rx.var
    def valid_row_count(self) -> int:
        return len([r for r in self.pending_rows if r["error"] == ""])

    @rx.var
    def invalid_row_count(self) -> int:
        return len([r for r in self.pending_rows if r["error"] != ""])

    @rx.var
    def has_pending(self) -> bool:
        return len(self.pending_rows) > 0

    @rx.event
    async def handle_csv_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        file = files[0]
        try:
            data = await file.read()
            text = data.decode("utf-8", errors="replace")
            reader = csv.DictReader(io.StringIO(text))
            rows: list[MigrationRow] = []
            from app.states.inventory_state import InventoryState

            inv = await self.get_state(InventoryState)
            valid_skus = {i["sku"]: i for i in inv.items}

            for idx, raw in enumerate(reader, start=1):
                sku = (raw.get("sku") or raw.get("SKU") or "").strip()
                qty_str = (raw.get("quantity") or raw.get("qty") or "0").strip()
                expiry = (
                    raw.get("expiry") or raw.get("expiry_date") or ""
                ).strip()
                location = (
                    raw.get("location") or ""
                ).strip() or MIGRATION_LOCATION
                lot = (raw.get("lot_number") or "").strip()
                err = ""
                qty_val = 0.0
                item_name = ""
                unit = ""
                try:
                    qty_val = float(qty_str)
                    if qty_val < 0:
                        err = "Negative opening balance not allowed"
                except ValueError:
                    err = "Invalid quantity"

                if sku not in valid_skus:
                    err = f"Unknown SKU: {sku}"
                else:
                    item_name = valid_skus[sku]["name"]
                    unit = valid_skus[sku]["unit"]

                if not lot:
                    lot = f"{MIGRATION_LOT_PREFIX}-{sku}-{idx:03d}"
                else:
                    if not lot.startswith(MIGRATION_LOT_PREFIX):
                        lot = f"{MIGRATION_LOT_PREFIX}-{lot}"

                rows.append(
                    {
                        "row_no": idx,
                        "sku": sku,
                        "item_name": item_name,
                        "quantity": qty_val,
                        "unit": unit,
                        "expiry": expiry or "—",
                        "location": location,
                        "lot_number": lot,
                        "status": MIGRATION_STATUS,
                        "error": err,
                    }
                )
            self.pending_rows = rows
            self.last_uploaded_file = file.name
            self.last_message = f"Parsed {len(rows)} rows from {file.name}"
            yield rx.toast.success(self.last_message)
        except Exception as e:
            logging.exception(f"Error parsing migration CSV: {e}")
            yield rx.toast.error(f"Failed to parse CSV: {e}")

    @rx.event
    def load_sample_csv(self):
        sample: list[MigrationRow] = [
            {
                "row_no": 1,
                "sku": "RGT-MTH-001",
                "item_name": "Methanol HPLC Grade",
                "quantity": 10.0,
                "unit": "L",
                "expiry": "2026-08-01",
                "location": MIGRATION_LOCATION,
                "lot_number": f"{MIGRATION_LOT_PREFIX}-RGT-MTH-001-001",
                "status": MIGRATION_STATUS,
                "error": "",
            },
            {
                "row_no": 2,
                "sku": "STD-PAR-003",
                "item_name": "Paracetamol Reference Standard",
                "quantity": 1.5,
                "unit": "g",
                "expiry": "2025-05-15",
                "location": MIGRATION_LOCATION,
                "lot_number": f"{MIGRATION_LOT_PREFIX}-STD-PAR-003-002",
                "status": MIGRATION_STATUS,
                "error": "",
            },
            {
                "row_no": 3,
                "sku": "UNKNOWN-SKU",
                "item_name": "",
                "quantity": 5.0,
                "unit": "",
                "expiry": "—",
                "location": MIGRATION_LOCATION,
                "lot_number": f"{MIGRATION_LOT_PREFIX}-UNKNOWN-003",
                "status": MIGRATION_STATUS,
                "error": "Unknown SKU: UNKNOWN-SKU",
            },
        ]
        self.pending_rows = sample
        self.last_uploaded_file = "sample_opening_balances.csv"
        return rx.toast.success("Sample preview loaded")

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

        if not self.pending_rows:
            yield rx.toast.error("No rows to import.")
            return
        valid_rows = [r for r in self.pending_rows if r["error"] == ""]
        if not valid_rows:
            yield rx.toast.error("No valid rows to import.")
            return

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)
        ops = await self.get_state(OperationsState)

        imported = 0
        for r in valid_rows:
            target = next((i for i in inv.items if i["sku"] == r["sku"]), None)
            if target is None:
                continue
            # Service-layer rule: opening balance is a positive credit; never negative
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
                from datetime import date as _date

                if r["expiry"] not in ("", "—"):
                    yyyy, mm, dd = r["expiry"].split("-")
                    days = (
                        _date(int(yyyy), int(mm), int(dd)) - _date.today()
                    ).days
                else:
                    days = 365
            except Exception:
                logging.exception("Migration expiry parse error")
                days = 365

            inv.lots.insert(
                0,
                {
                    "id": f"LOT-{uuid.uuid4().hex[:6].upper()}",
                    "item_id": target["id"],
                    "item_name": target["name"],
                    "lot_number": r["lot_number"],
                    "quantity": r["quantity"],
                    "unit": r["unit"],
                    "received_date": datetime.now().strftime("%Y-%m-%d"),
                    "expiry_date": r["expiry"]
                    if r["expiry"] != "—"
                    else "2099-12-31",
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
                f"Migrated {r['quantity']} {r['unit']} → {r['location']} (Released)",
            )
            imported += 1

        new_batch: MigrationBatch = {
            "id": f"MIG-{uuid.uuid4().hex[:6].upper()}",
            "batch_no": f"MIG-2024-{1 + len(self.batches):04d}",
            "file_name": self.last_uploaded_file or "manual_entry",
            "rows_total": len(self.pending_rows),
            "rows_valid": len(valid_rows),
            "rows_invalid": len(self.pending_rows) - len(valid_rows),
            "rows_imported": imported,
            "submitted_by": auth.current_user,
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Imported",
        }
        self.batches.insert(0, new_batch)
        self.pending_rows = []
        self.last_uploaded_file = ""
        self.last_message = f"Imported {imported} opening balances"
        yield rx.toast.success(self.last_message)