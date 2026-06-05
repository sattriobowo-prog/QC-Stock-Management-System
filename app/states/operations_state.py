import reflex as rx
from typing import TypedDict
from datetime import datetime
import uuid
import logging


class MaterialRequest(TypedDict):
    id: str
    request_no: str
    requester: str
    purpose: str
    item_id: str
    item_name: str
    item_sku: str
    quantity: float
    unit: str
    is_napza: bool
    is_hazard: bool
    status: str
    priority: str
    created_at: str
    notes: str


class IssueRecord(TypedDict):
    id: str
    issue_no: str
    item_id: str
    item_name: str
    lot_number: str
    quantity: float
    unit: str
    issued_to: str
    purpose: str
    override_reason: str
    issued_by: str
    issued_at: str


class ReceivingRecord(TypedDict):
    id: str
    receiving_no: str
    po_number: str
    vendor: str
    item_id: str
    item_name: str
    lot_number: str
    quantity: float
    unit: str
    received_date: str
    expiry_date: str
    status: str
    document_ref: str
    received_by: str
    notes: str


class Adjustment(TypedDict):
    id: str
    adjustment_no: str
    item_id: str
    item_name: str
    delta: float
    unit: str
    reason: str
    submitter: str
    approver: str
    status: str
    created_at: str
    approved_at: str
    notes: str


class AuditEntry(TypedDict):
    id: str
    timestamp: str
    user: str
    role: str
    action: str
    target: str
    detail: str


class OperationsState(rx.State):
    requests: list[MaterialRequest] = [
        {
            "id": "REQ-001",
            "request_no": "MR-2024-1101",
            "requester": "Dr. Sarah Chen",
            "purpose": "Assay validation - Paracetamol tablets",
            "item_id": "ITM-003",
            "item_name": "Paracetamol Reference Standard",
            "item_sku": "STD-PAR-003",
            "quantity": 0.5,
            "unit": "g",
            "is_napza": False,
            "is_hazard": False,
            "status": "Approved",
            "priority": "Normal",
            "created_at": "2024-11-11 09:24",
            "notes": "Required for monthly calibration run",
        },
        {
            "id": "REQ-002",
            "request_no": "MR-2024-1102",
            "requester": "John Martinez",
            "purpose": "Mobile phase preparation",
            "item_id": "ITM-001",
            "item_name": "Methanol HPLC Grade",
            "item_sku": "RGT-MTH-001",
            "quantity": 5.0,
            "unit": "L",
            "is_napza": False,
            "is_hazard": True,
            "status": "Pending Approval",
            "priority": "High",
            "created_at": "2024-11-12 11:08",
            "notes": "HPLC method development",
        },
        {
            "id": "REQ-003",
            "request_no": "MR-2024-1103",
            "requester": "Emily Rodriguez",
            "purpose": "Forensic toxicology analysis",
            "item_id": "ITM-004",
            "item_name": "Morphine Sulfate Standard",
            "item_sku": "NPZ-MOR-004",
            "quantity": 50.0,
            "unit": "mg",
            "is_napza": True,
            "is_hazard": True,
            "status": "Pending Approval",
            "priority": "High",
            "created_at": "2024-11-13 08:45",
            "notes": "NAPZA registry approval required",
        },
        {
            "id": "REQ-004",
            "request_no": "MR-2024-1104",
            "requester": "Akira Tanaka",
            "purpose": "Routine pH buffer prep",
            "item_id": "ITM-005",
            "item_name": "Phosphate Buffer pH 6.8",
            "item_sku": "RGT-PHB-005",
            "quantity": 2.0,
            "unit": "L",
            "is_napza": False,
            "is_hazard": False,
            "status": "Issued",
            "priority": "Normal",
            "created_at": "2024-11-08 14:12",
            "notes": "",
        },
        {
            "id": "REQ-005",
            "request_no": "MR-2024-1105",
            "requester": "Mei-Lin Zhao",
            "purpose": "Titration standard prep",
            "item_id": "ITM-008",
            "item_name": "Sodium Hydroxide 0.1N",
            "item_sku": "RGT-NAOH-008",
            "quantity": 1.0,
            "unit": "L",
            "is_napza": False,
            "is_hazard": True,
            "status": "Rejected",
            "priority": "Low",
            "created_at": "2024-11-07 16:30",
            "notes": "Insufficient justification for restricted reagent",
        },
    ]

    issues: list[IssueRecord] = [
        {
            "id": "ISS-001",
            "issue_no": "IS-2024-2201",
            "item_id": "ITM-005",
            "item_name": "Phosphate Buffer pH 6.8",
            "lot_number": "PHB-INT-241101",
            "quantity": 2.0,
            "unit": "L",
            "issued_to": "Akira Tanaka",
            "purpose": "Routine pH buffer prep",
            "override_reason": "",
            "issued_by": "Warehouse Officer",
            "issued_at": "2024-11-08 14:30",
        },
        {
            "id": "ISS-002",
            "issue_no": "IS-2024-2202",
            "item_id": "ITM-001",
            "item_name": "Methanol HPLC Grade",
            "lot_number": "MTH240801-A",
            "quantity": 4.0,
            "unit": "L",
            "issued_to": "John Martinez",
            "purpose": "HPLC mobile phase",
            "override_reason": "",
            "issued_by": "Warehouse Officer",
            "issued_at": "2024-11-10 09:50",
        },
        {
            "id": "ISS-003",
            "issue_no": "IS-2024-2203",
            "item_id": "ITM-003",
            "item_name": "Paracetamol Reference Standard",
            "lot_number": "PAR-USP-2024-05",
            "quantity": 0.25,
            "unit": "g",
            "issued_to": "Dr. Sarah Chen",
            "purpose": "Assay validation",
            "override_reason": "Selected non-FEFO lot for matched validation set",
            "issued_by": "QC Manager",
            "issued_at": "2024-11-11 10:15",
        },
    ]

    receivings: list[ReceivingRecord] = [
        {
            "id": "RCV-001",
            "receiving_no": "GR-2024-3301",
            "po_number": "PO-2024-0451",
            "vendor": "Merck KGaA",
            "item_id": "ITM-001",
            "item_name": "Methanol HPLC Grade",
            "lot_number": "MTH241015-B",
            "quantity": 20.5,
            "unit": "L",
            "received_date": "2024-10-15",
            "expiry_date": "2026-10-15",
            "status": "Released",
            "document_ref": "COA-MRK-241015.pdf",
            "received_by": "Warehouse Officer",
            "notes": "QC released after COA review",
        },
        {
            "id": "RCV-002",
            "receiving_no": "GR-2024-3302",
            "po_number": "PO-2024-0488",
            "vendor": "Sigma-Aldrich",
            "item_id": "ITM-009",
            "item_name": "Ibuprofen Working Standard",
            "lot_number": "IBU-SIG-241113",
            "quantity": 2.1,
            "unit": "g",
            "received_date": "2024-11-13",
            "expiry_date": "2025-11-13",
            "status": "Pending Release",
            "document_ref": "COA-SIG-241113.pdf",
            "received_by": "Warehouse Officer",
            "notes": "Awaiting QC release sign-off",
        },
        {
            "id": "RCV-003",
            "receiving_no": "GR-2024-3303",
            "po_number": "PO-2024-0501",
            "vendor": "Internal Prep",
            "item_id": "ITM-008",
            "item_name": "Sodium Hydroxide 0.1N",
            "lot_number": "NAOH-INT-241105",
            "quantity": 15.0,
            "unit": "L",
            "received_date": "2024-11-05",
            "expiry_date": "2025-02-05",
            "status": "Released",
            "document_ref": "PREP-LOG-241105.pdf",
            "received_by": "QC Analyst",
            "notes": "Internally prepared and standardized",
        },
    ]

    adjustments: list[Adjustment] = [
        {
            "id": "ADJ-001",
            "adjustment_no": "ADJ-2024-4401",
            "item_id": "ITM-002",
            "item_name": "Acetonitrile HPLC Grade",
            "delta": -1.5,
            "unit": "L",
            "reason": "Spillage during dispense",
            "submitter": "John Martinez",
            "approver": "Dr. Sarah Chen",
            "status": "Approved",
            "created_at": "2024-11-09 13:20",
            "approved_at": "2024-11-09 15:45",
            "notes": "Incident report INC-2024-019 filed",
        },
        {
            "id": "ADJ-002",
            "adjustment_no": "ADJ-2024-4402",
            "item_id": "ITM-006",
            "item_name": "Volumetric Flask 100mL Class A",
            "delta": -2.0,
            "unit": "pcs",
            "reason": "Breakage during analysis",
            "submitter": "Akira Tanaka",
            "approver": "",
            "status": "Pending Approval",
            "created_at": "2024-11-12 10:05",
            "approved_at": "",
            "notes": "Replacement requested",
        },
        {
            "id": "ADJ-003",
            "adjustment_no": "ADJ-2024-4403",
            "item_id": "ITM-010",
            "item_name": "PTFE Syringe Filter 0.45μm",
            "delta": 5.0,
            "unit": "pcs",
            "reason": "Cycle count correction",
            "submitter": "Warehouse Officer",
            "approver": "",
            "status": "Pending Approval",
            "created_at": "2024-11-13 09:00",
            "approved_at": "",
            "notes": "Found in secondary cabinet during count",
        },
    ]

    audit_log: list[AuditEntry] = [
        {
            "id": "AUD-001",
            "timestamp": "2024-11-08 14:30",
            "user": "Warehouse Officer",
            "role": "Warehouse Officer",
            "action": "ISSUE",
            "target": "ITM-005 / PHB-INT-241101",
            "detail": "Issued 2.0 L to Akira Tanaka (FEFO)",
        },
        {
            "id": "AUD-002",
            "timestamp": "2024-11-09 15:45",
            "user": "Dr. Sarah Chen",
            "role": "QC Manager",
            "action": "ADJUSTMENT_APPROVED",
            "target": "ITM-002",
            "detail": "Approved -1.5 L spillage adjustment",
        },
        {
            "id": "AUD-003",
            "timestamp": "2024-11-13 08:45",
            "user": "Emily Rodriguez",
            "role": "QC Analyst",
            "action": "REQUEST_CREATED",
            "target": "ITM-004",
            "detail": "Requested 50 mg NAPZA standard",
        },
    ]

    # Material Request form
    mr_item_id: str = ""
    mr_quantity: str = ""
    mr_purpose: str = ""
    mr_priority: str = "Normal"
    mr_notes: str = ""

    # Issue form
    issue_item_id: str = ""
    issue_quantity: str = ""
    issue_recipient: str = ""
    issue_purpose: str = ""
    issue_lot_override: str = ""
    issue_override_reason: str = ""

    # Receiving form
    rcv_item_id: str = ""
    rcv_po_number: str = ""
    rcv_vendor: str = ""
    rcv_lot_number: str = ""
    rcv_quantity: str = ""
    rcv_expiry: str = ""
    rcv_document_ref: str = ""
    rcv_notes: str = ""

    # Adjustment form
    adj_item_id: str = ""
    adj_delta: str = ""
    adj_reason: str = ""
    adj_notes: str = ""

    request_status_filter: str = "All"
    last_message: str = ""
    last_message_kind: str = ""

    @rx.var
    def filtered_requests(self) -> list[MaterialRequest]:
        if self.request_status_filter == "All":
            return self.requests
        return [
            r
            for r in self.requests
            if r["status"] == self.request_status_filter
        ]

    @rx.var
    def pending_request_count(self) -> int:
        return len(
            [r for r in self.requests if r["status"] == "Pending Approval"]
        )

    @rx.var
    def pending_adjustment_count(self) -> int:
        return len(
            [a for a in self.adjustments if a["status"] == "Pending Approval"]
        )

    @rx.var
    def pending_release_count(self) -> int:
        return len(
            [r for r in self.receivings if r["status"] == "Pending Release"]
        )

    @rx.var
    async def fefo_lots_for_issue(self) -> list[dict]:
        """Service-layer FEFO selection: only Released lots, sorted by expiry."""
        from app.states.inventory_state import InventoryState

        inv = await self.get_state(InventoryState)
        if not self.issue_item_id:
            return []
        candidates = [
            l
            for l in inv.lots
            if l["item_id"] == self.issue_item_id
            and l["status"] == "Released"
            and l["quantity"] > 0
        ]
        candidates.sort(key=lambda x: x["days_to_expiry"])
        return [
            {
                "lot_number": l["lot_number"],
                "quantity": l["quantity"],
                "unit": l["unit"],
                "expiry_date": l["expiry_date"],
                "days_to_expiry": l["days_to_expiry"],
            }
            for l in candidates
        ]

    @rx.var
    async def selected_issue_item(self) -> dict:
        from app.states.inventory_state import InventoryState

        inv = await self.get_state(InventoryState)
        for i in inv.items:
            if i["id"] == self.issue_item_id:
                return {
                    "name": i["name"],
                    "sku": i["sku"],
                    "unit": i["unit"],
                    "available": i["available"],
                    "is_napza": i["is_napza"],
                    "is_hazard": i["is_hazard"],
                    "status": i["status"],
                }
        return {
            "name": "",
            "sku": "",
            "unit": "",
            "available": 0.0,
            "is_napza": False,
            "is_hazard": False,
            "status": "",
        }

    @rx.var
    async def selected_mr_item(self) -> dict:
        from app.states.inventory_state import InventoryState

        inv = await self.get_state(InventoryState)
        for i in inv.items:
            if i["id"] == self.mr_item_id:
                return {
                    "name": i["name"],
                    "sku": i["sku"],
                    "unit": i["unit"],
                    "available": i["available"],
                    "is_napza": i["is_napza"],
                    "is_hazard": i["is_hazard"],
                }
        return {
            "name": "",
            "sku": "",
            "unit": "",
            "available": 0.0,
            "is_napza": False,
            "is_hazard": False,
        }

    @rx.var
    async def item_options(self) -> list[dict]:
        from app.states.inventory_state import InventoryState

        inv = await self.get_state(InventoryState)
        return [
            {"id": i["id"], "label": f"{i['sku']} — {i['name']}"}
            for i in inv.items
        ]

    # ---------- Setters ----------
    @rx.event
    def set_mr_item(self, v: str):
        self.mr_item_id = v

    @rx.event
    def set_mr_quantity(self, v: str):
        self.mr_quantity = v

    @rx.event
    def set_mr_purpose(self, v: str):
        self.mr_purpose = v

    @rx.event
    def set_mr_priority(self, v: str):
        self.mr_priority = v

    @rx.event
    def set_mr_notes(self, v: str):
        self.mr_notes = v

    @rx.event
    def set_issue_item(self, v: str):
        self.issue_item_id = v
        self.issue_lot_override = ""

    @rx.event
    def set_issue_quantity(self, v: str):
        self.issue_quantity = v

    @rx.event
    def set_issue_recipient(self, v: str):
        self.issue_recipient = v

    @rx.event
    def set_issue_purpose(self, v: str):
        self.issue_purpose = v

    @rx.event
    def set_issue_lot_override(self, v: str):
        self.issue_lot_override = v

    @rx.event
    def set_issue_override_reason(self, v: str):
        self.issue_override_reason = v

    @rx.event
    def set_rcv_item(self, v: str):
        self.rcv_item_id = v

    @rx.event
    def set_rcv_po(self, v: str):
        self.rcv_po_number = v

    @rx.event
    def set_rcv_vendor(self, v: str):
        self.rcv_vendor = v

    @rx.event
    def set_rcv_lot(self, v: str):
        self.rcv_lot_number = v

    @rx.event
    def set_rcv_quantity(self, v: str):
        self.rcv_quantity = v

    @rx.event
    def set_rcv_expiry(self, v: str):
        self.rcv_expiry = v

    @rx.event
    def set_rcv_document(self, v: str):
        self.rcv_document_ref = v

    @rx.event
    def set_rcv_notes(self, v: str):
        self.rcv_notes = v

    @rx.event
    def set_adj_item(self, v: str):
        self.adj_item_id = v

    @rx.event
    def set_adj_delta(self, v: str):
        self.adj_delta = v

    @rx.event
    def set_adj_reason(self, v: str):
        self.adj_reason = v

    @rx.event
    def set_adj_notes(self, v: str):
        self.adj_notes = v

    @rx.event
    def set_request_filter(self, v: str):
        self.request_status_filter = v

    # ---------- Service-layer helpers ----------
    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def _audit(
        self, user: str, role: str, action: str, target: str, detail: str
    ):
        self.audit_log.insert(
            0,
            {
                "id": f"AUD-{uuid.uuid4().hex[:8].upper()}",
                "timestamp": self._now(),
                "user": user,
                "role": role,
                "action": action,
                "target": target,
                "detail": detail,
            },
        )

    def _validate_stock_change(
        self, item_id: str, delta: float, items: list
    ) -> tuple[bool, str, dict | None]:
        for i in items:
            if i["id"] == item_id:
                new_qty = i["on_hand"] + delta
                if new_qty < 0:
                    return (
                        False,
                        f"Operation rejected: would result in negative stock ({new_qty:.3f} {i['unit']}).",
                        None,
                    )
                return (True, "OK", i)
        return (False, f"Item {item_id} not found.", None)

    # ---------- Material Request submission ----------
    @rx.event
    async def submit_material_request(self):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState

        if not self.mr_item_id:
            self.last_message = "Please select an item."
            self.last_message_kind = "error"
            yield rx.toast.error("Please select an item.")
            return
        try:
            qty = float(self.mr_quantity)
        except ValueError:
            self.last_message = "Invalid quantity."
            self.last_message_kind = "error"
            yield rx.toast.error("Invalid quantity.")
            return
        if qty <= 0:
            self.last_message = "Quantity must be positive."
            self.last_message_kind = "error"
            yield rx.toast.error("Quantity must be positive.")
            return
        if not self.mr_purpose.strip():
            self.last_message = "Purpose is required."
            self.last_message_kind = "error"
            yield rx.toast.error("Purpose is required.")
            return

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)
        item = next((i for i in inv.items if i["id"] == self.mr_item_id), None)
        if item is None:
            yield rx.toast.error("Item not found.")
            return

        new_no = f"MR-2024-{1100 + len(self.requests) + 10}"
        new_req: MaterialRequest = {
            "id": f"REQ-{uuid.uuid4().hex[:6].upper()}",
            "request_no": new_no,
            "requester": auth.current_user,
            "purpose": self.mr_purpose,
            "item_id": item["id"],
            "item_name": item["name"],
            "item_sku": item["sku"],
            "quantity": qty,
            "unit": item["unit"],
            "is_napza": item["is_napza"],
            "is_hazard": item["is_hazard"],
            "status": "Pending Approval",
            "priority": self.mr_priority,
            "created_at": self._now(),
            "notes": self.mr_notes,
        }
        self.requests.insert(0, new_req)
        self._audit(
            auth.current_user,
            auth.current_role,
            "REQUEST_CREATED",
            item["id"],
            f"Requested {qty} {item['unit']} — {self.mr_purpose}",
        )

        self.mr_item_id = ""
        self.mr_quantity = ""
        self.mr_purpose = ""
        self.mr_notes = ""
        self.mr_priority = "Normal"
        self.last_message = f"Request {new_no} submitted for approval."
        self.last_message_kind = "success"
        yield rx.toast.success(f"Request {new_no} submitted")

    @rx.event
    async def approve_request(self, req_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        for r in self.requests:
            if r["id"] == req_id:
                if r["requester"] == auth.current_user:
                    yield rx.toast.error("Self-approval is not permitted.")
                    return
                r["status"] = "Approved"
                self._audit(
                    auth.current_user,
                    auth.current_role,
                    "REQUEST_APPROVED",
                    r["item_id"],
                    f"Approved request {r['request_no']}",
                )
                yield rx.toast.success(f"Request {r['request_no']} approved")
                return

    @rx.event
    async def reject_request(self, req_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        for r in self.requests:
            if r["id"] == req_id:
                if r["requester"] == auth.current_user:
                    yield rx.toast.error("Self-rejection is not permitted.")
                    return
                r["status"] = "Rejected"
                self._audit(
                    auth.current_user,
                    auth.current_role,
                    "REQUEST_REJECTED",
                    r["item_id"],
                    f"Rejected request {r['request_no']}",
                )
                yield rx.toast(f"Request {r['request_no']} rejected")
                return

    # ---------- Issue / Consume ----------
    @rx.event
    async def submit_issue(self):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState

        if not self.issue_item_id:
            yield rx.toast.error("Select an item to issue.")
            return
        try:
            qty = float(self.issue_quantity)
        except ValueError:
            yield rx.toast.error("Invalid quantity.")
            return
        if qty <= 0:
            yield rx.toast.error("Quantity must be positive.")
            return
        if not self.issue_recipient.strip():
            yield rx.toast.error("Recipient required.")
            return
        if not self.issue_purpose.strip():
            yield rx.toast.error("Purpose required.")
            return

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)

        # Service-layer: only Released, positive lots; FEFO unless override
        candidate_lots = sorted(
            [
                l
                for l in inv.lots
                if l["item_id"] == self.issue_item_id
                and l["status"] == "Released"
                and l["quantity"] > 0
            ],
            key=lambda x: x["days_to_expiry"],
        )
        if not candidate_lots:
            yield rx.toast.error("No Released lots available for issue.")
            return

        chosen_lot = None
        if self.issue_lot_override:
            chosen_lot = next(
                (
                    l
                    for l in candidate_lots
                    if l["lot_number"] == self.issue_lot_override
                ),
                None,
            )
            if chosen_lot is None:
                yield rx.toast.error(
                    "Selected lot not eligible (must be Released)."
                )
                return
            if chosen_lot["lot_number"] != candidate_lots[0]["lot_number"]:
                if not self.issue_override_reason.strip():
                    yield rx.toast.error(
                        "Override reason required when bypassing FEFO."
                    )
                    return
        else:
            chosen_lot = candidate_lots[0]

        if chosen_lot["quantity"] < qty:
            yield rx.toast.error(
                f"Lot {chosen_lot['lot_number']} only has {chosen_lot['quantity']} {chosen_lot['unit']}."
            )
            return

        ok, msg, item = self._validate_stock_change(
            self.issue_item_id, -qty, inv.items
        )
        if not ok:
            yield rx.toast.error(msg)
            return

        # Apply through service layer (mutate inventory state)
        item["on_hand"] = round(item["on_hand"] - qty, 4)
        item["available"] = round(item["available"] - qty, 4)
        item["total_issued"] = round(item["total_issued"] + qty, 4)
        item["last_issued_date"] = self._now().split(" ")[0]
        item["last_updated"] = self._now().split(" ")[0]
        if item["on_hand"] <= 0:
            item["status"] = "Out of Stock"

        for l in inv.lots:
            if l["lot_number"] == chosen_lot["lot_number"]:
                l["quantity"] = round(l["quantity"] - qty, 4)
                break

        new_iss: IssueRecord = {
            "id": f"ISS-{uuid.uuid4().hex[:6].upper()}",
            "issue_no": f"IS-2024-{2200 + len(self.issues) + 10}",
            "item_id": item["id"],
            "item_name": item["name"],
            "lot_number": chosen_lot["lot_number"],
            "quantity": qty,
            "unit": item["unit"],
            "issued_to": self.issue_recipient,
            "purpose": self.issue_purpose,
            "override_reason": self.issue_override_reason,
            "issued_by": auth.current_user,
            "issued_at": self._now(),
        }
        self.issues.insert(0, new_iss)
        self._audit(
            auth.current_user,
            auth.current_role,
            "ISSUE",
            f"{item['id']} / {chosen_lot['lot_number']}",
            f"Issued {qty} {item['unit']} to {self.issue_recipient}"
            + (
                f" [override: {self.issue_override_reason}]"
                if self.issue_override_reason
                else " (FEFO)"
            ),
        )

        self.issue_quantity = ""
        self.issue_recipient = ""
        self.issue_purpose = ""
        self.issue_lot_override = ""
        self.issue_override_reason = ""
        yield rx.toast.success(f"Issued {qty} {item['unit']} of {item['name']}")

    # ---------- Receiving ----------
    @rx.event
    async def submit_receiving(self):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState

        if not self.rcv_item_id:
            yield rx.toast.error("Select an item.")
            return
        if not self.rcv_lot_number.strip():
            yield rx.toast.error("Lot number required.")
            return
        try:
            qty = float(self.rcv_quantity)
        except ValueError:
            yield rx.toast.error("Invalid quantity.")
            return
        if qty <= 0:
            yield rx.toast.error("Quantity must be positive.")
            return
        if not self.rcv_expiry.strip():
            yield rx.toast.error("Expiry date required.")
            return

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)
        item = next((i for i in inv.items if i["id"] == self.rcv_item_id), None)
        if item is None:
            yield rx.toast.error("Item not found.")
            return

        # Service-layer: receivings default to Pending Release
        new_rcv: ReceivingRecord = {
            "id": f"RCV-{uuid.uuid4().hex[:6].upper()}",
            "receiving_no": f"GR-2024-{3300 + len(self.receivings) + 10}",
            "po_number": self.rcv_po_number or "—",
            "vendor": self.rcv_vendor or item["vendor"],
            "item_id": item["id"],
            "item_name": item["name"],
            "lot_number": self.rcv_lot_number,
            "quantity": qty,
            "unit": item["unit"],
            "received_date": self._now().split(" ")[0],
            "expiry_date": self.rcv_expiry,
            "status": "Pending Release",
            "document_ref": self.rcv_document_ref or "—",
            "received_by": auth.current_user,
            "notes": self.rcv_notes,
        }
        self.receivings.insert(0, new_rcv)

        # Add new lot in Pending Release; on_hand only updates upon release per QC rules
        try:
            from datetime import date as _date

            yyyy, mm, dd = self.rcv_expiry.split("-")
            exp = _date(int(yyyy), int(mm), int(dd))
            days = (exp - _date.today()).days
        except Exception:
            logging.exception("Unexpected error")
            days = 365

        inv.lots.insert(
            0,
            {
                "id": f"LOT-{uuid.uuid4().hex[:6].upper()}",
                "item_id": item["id"],
                "item_name": item["name"],
                "lot_number": self.rcv_lot_number,
                "quantity": qty,
                "unit": item["unit"],
                "received_date": new_rcv["received_date"],
                "expiry_date": self.rcv_expiry,
                "status": "Pending Release",
                "location": item["location"],
                "vendor": new_rcv["vendor"],
                "days_to_expiry": days,
            },
        )
        item["incoming"] = round(item["incoming"] + qty, 4)
        item["last_updated"] = new_rcv["received_date"]

        self._audit(
            auth.current_user,
            auth.current_role,
            "RECEIVING",
            f"{item['id']} / {self.rcv_lot_number}",
            f"Received {qty} {item['unit']} from {new_rcv['vendor']} (Pending Release)",
        )

        self.rcv_item_id = ""
        self.rcv_po_number = ""
        self.rcv_vendor = ""
        self.rcv_lot_number = ""
        self.rcv_quantity = ""
        self.rcv_expiry = ""
        self.rcv_document_ref = ""
        self.rcv_notes = ""
        yield rx.toast.success(
            f"Received {qty} {item['unit']} (Pending Release)"
        )

    @rx.event
    async def release_receiving(self, rcv_id: str):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)

        for r in self.receivings:
            if r["id"] == rcv_id:
                if r["status"] != "Pending Release":
                    yield rx.toast("Already released.")
                    return
                if r["received_by"] == auth.current_user:
                    yield rx.toast.error("Self-release not permitted.")
                    return
                r["status"] = "Released"
                # Update lot status and item on_hand
                for l in inv.lots:
                    if l["lot_number"] == r["lot_number"]:
                        l["status"] = "Released"
                for i in inv.items:
                    if i["id"] == r["item_id"]:
                        i["on_hand"] = round(i["on_hand"] + r["quantity"], 4)
                        i["available"] = round(
                            i["available"] + r["quantity"], 4
                        )
                        i["incoming"] = round(
                            max(0.0, i["incoming"] - r["quantity"]), 4
                        )
                        i["total_received"] = round(
                            i["total_received"] + r["quantity"], 4
                        )
                        i["last_received_date"] = r["received_date"]
                        i["last_updated"] = self._now().split(" ")[0]
                        if i["status"] == "Out of Stock":
                            i["status"] = "Released"
                self._audit(
                    auth.current_user,
                    auth.current_role,
                    "RECEIVING_RELEASED",
                    f"{r['item_id']} / {r['lot_number']}",
                    f"Released {r['quantity']} {r['unit']} into available stock",
                )
                yield rx.toast.success(f"Released {r['receiving_no']}")
                return

    # ---------- Adjustments ----------
    @rx.event
    async def submit_adjustment(self):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState

        if not self.adj_item_id:
            yield rx.toast.error("Select an item.")
            return
        try:
            delta = float(self.adj_delta)
        except ValueError:
            yield rx.toast.error("Invalid delta value.")
            return
        if delta == 0:
            yield rx.toast.error("Delta cannot be zero.")
            return
        if not self.adj_reason.strip():
            yield rx.toast.error("Reason is required.")
            return

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)

        # Pre-validate (won't apply until approved, but warn early)
        ok, msg, _ = self._validate_stock_change(
            self.adj_item_id, delta, inv.items
        )
        if not ok:
            yield rx.toast.error(msg)
            return

        item = next(i for i in inv.items if i["id"] == self.adj_item_id)
        new_adj: Adjustment = {
            "id": f"ADJ-{uuid.uuid4().hex[:6].upper()}",
            "adjustment_no": f"ADJ-2024-{4400 + len(self.adjustments) + 10}",
            "item_id": item["id"],
            "item_name": item["name"],
            "delta": delta,
            "unit": item["unit"],
            "reason": self.adj_reason,
            "submitter": auth.current_user,
            "approver": "",
            "status": "Pending Approval",
            "created_at": self._now(),
            "approved_at": "",
            "notes": self.adj_notes,
        }
        self.adjustments.insert(0, new_adj)
        self._audit(
            auth.current_user,
            auth.current_role,
            "ADJUSTMENT_CREATED",
            item["id"],
            f"Submitted Δ{delta} {item['unit']} — {self.adj_reason}",
        )

        self.adj_item_id = ""
        self.adj_delta = ""
        self.adj_reason = ""
        self.adj_notes = ""
        yield rx.toast.success(
            f"Adjustment {new_adj['adjustment_no']} submitted"
        )

    @rx.event
    async def approve_adjustment(self, adj_id: str):
        from app.states.inventory_state import InventoryState
        from app.states.auth_state import AuthState

        inv = await self.get_state(InventoryState)
        auth = await self.get_state(AuthState)

        for a in self.adjustments:
            if a["id"] == adj_id:
                if a["submitter"] == auth.current_user:
                    yield rx.toast.error("Self-approval is not permitted.")
                    return
                if a["status"] != "Pending Approval":
                    yield rx.toast("Already processed.")
                    return
                ok, msg, item = self._validate_stock_change(
                    a["item_id"], a["delta"], inv.items
                )
                if not ok:
                    yield rx.toast.error(msg)
                    return
                item["on_hand"] = round(item["on_hand"] + a["delta"], 4)
                item["available"] = round(item["available"] + a["delta"], 4)
                item["last_updated"] = self._now().split(" ")[0]
                if item["on_hand"] <= 0:
                    item["status"] = "Out of Stock"
                a["status"] = "Approved"
                a["approver"] = auth.current_user
                a["approved_at"] = self._now()
                self._audit(
                    auth.current_user,
                    auth.current_role,
                    "ADJUSTMENT_APPROVED",
                    a["item_id"],
                    f"Applied Δ{a['delta']} {a['unit']}",
                )
                yield rx.toast.success(
                    f"Adjustment {a['adjustment_no']} approved"
                )
                return

    @rx.event
    async def reject_adjustment(self, adj_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        for a in self.adjustments:
            if a["id"] == adj_id:
                if a["submitter"] == auth.current_user:
                    yield rx.toast.error("Self-rejection not permitted.")
                    return
                a["status"] = "Rejected"
                a["approver"] = auth.current_user
                a["approved_at"] = self._now()
                self._audit(
                    auth.current_user,
                    auth.current_role,
                    "ADJUSTMENT_REJECTED",
                    a["item_id"],
                    f"Rejected Δ{a['delta']} {a['unit']}",
                )
                yield rx.toast(f"Adjustment {a['adjustment_no']} rejected")
                return