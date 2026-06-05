import reflex as rx
from typing import TypedDict
from datetime import datetime
import uuid
from app.services.vendor_service import (
    mask_vendor_list,
    can_edit_vendor,
)
from app.services.admin_service import can_perform_reset


class Vendor(TypedDict):
    id: str
    name: str
    code: str
    category: str
    contact_person: str
    email: str
    phone: str
    address: str
    status: str
    qualified: bool
    last_audit: str
    notes: str


class Document(TypedDict):
    id: str
    doc_no: str
    title: str
    category: str
    linked_to: str
    file_name: str
    uploaded_by: str
    uploaded_at: str
    expiry: str
    status: str


class DocumentCategory(TypedDict):
    id: str
    name: str
    description: str
    retention_days: int
    required_for: str


class ExpiryTask(TypedDict):
    id: str
    task_no: str
    item_name: str
    lot_number: str
    expiry_date: str
    days_to_expiry: int
    assigned_to: str
    status: str
    action: str
    completed_at: str


class Transfer(TypedDict):
    id: str
    transfer_no: str
    item_name: str
    lot_number: str
    quantity: float
    unit: str
    from_location: str
    to_location: str
    requested_by: str
    approved_by: str
    status: str
    created_at: str
    completed_at: str
    reason: str


class Notification(TypedDict):
    id: str
    timestamp: str
    severity: str
    title: str
    message: str
    target_role: str
    read: bool


class MasterDataRequest(TypedDict):
    id: str
    request_no: str
    entity: str
    target: str
    change_type: str
    proposed_value: str
    requester: str
    approver: str
    status: str
    created_at: str
    rationale: str


class SystemSetting(TypedDict):
    key: str
    label: str
    value: str
    category: str
    description: str


class GovernanceState(rx.State):
    vendors: list[Vendor] = [
        {
            "id": "VND-001",
            "name": "Merck KGaA",
            "code": "VEN-MRK",
            "category": "Reagent Manufacturer",
            "contact_person": "Hans Mueller",
            "email": "h.mueller@merck.de",
            "phone": "+49 6151 720",
            "address": "Frankfurter Strasse 250, Darmstadt, Germany",
            "status": "Active",
            "qualified": True,
            "last_audit": "2024-03-15",
            "notes": "Primary HPLC solvent supplier",
        },
        {
            "id": "VND-002",
            "name": "Sigma-Aldrich",
            "code": "VEN-SIG",
            "category": "Reagent Manufacturer",
            "contact_person": "Maria Lopez",
            "email": "m.lopez@sigmaaldrich.com",
            "phone": "+1 314 771 5765",
            "address": "3050 Spruce Street, St. Louis, MO, USA",
            "status": "Active",
            "qualified": True,
            "last_audit": "2024-06-21",
            "notes": "Reference standards and specialty reagents",
        },
        {
            "id": "VND-003",
            "name": "USP",
            "code": "VEN-USP",
            "category": "Reference Standard",
            "contact_person": "Robert King",
            "email": "rk@usp.org",
            "phone": "+1 301 881 0666",
            "address": "12601 Twinbrook Parkway, Rockville, MD, USA",
            "status": "Active",
            "qualified": True,
            "last_audit": "2024-01-10",
            "notes": "USP/NF reference standards",
        },
        {
            "id": "VND-004",
            "name": "Pyrex",
            "code": "VEN-PYR",
            "category": "Glassware",
            "contact_person": "Jennifer Park",
            "email": "j.park@pyrex.com",
            "phone": "+1 800 234 5678",
            "address": "1 Riverfront Plaza, Corning, NY, USA",
            "status": "Active",
            "qualified": True,
            "last_audit": "2023-11-22",
            "notes": "Class A volumetric glassware",
        },
        {
            "id": "VND-005",
            "name": "Millipore",
            "code": "VEN-MIL",
            "category": "Consumables",
            "contact_person": "Lin Wei",
            "email": "l.wei@millipore.com",
            "phone": "+1 978 715 4321",
            "address": "400 Summit Drive, Burlington, MA, USA",
            "status": "Active",
            "qualified": True,
            "last_audit": "2024-08-09",
            "notes": "Filtration consumables",
        },
        {
            "id": "VND-006",
            "name": "Internal Prep",
            "code": "VEN-INT",
            "category": "In-house",
            "contact_person": "QC Lab Internal",
            "email": "qclab@internal",
            "phone": "—",
            "address": "QC Laboratory, Building 4",
            "status": "Active",
            "qualified": True,
            "last_audit": "2024-10-01",
            "notes": "Internally prepared buffers and titrants",
        },
        {
            "id": "VND-007",
            "name": "Acme Reagents Ltd",
            "code": "VEN-ACM",
            "category": "Reagent Manufacturer",
            "contact_person": "Carlos Rivera",
            "email": "c.rivera@acmereag.co",
            "phone": "+1 555 222 9999",
            "address": "200 Industrial Blvd, Houston, TX, USA",
            "status": "Suspended",
            "qualified": False,
            "last_audit": "2023-05-04",
            "notes": "Quality issues — pending re-qualification",
        },
    ]

    documents: list[Document] = [
        {
            "id": "DOC-001",
            "doc_no": "COA-MRK-241015",
            "title": "Methanol HPLC Grade COA",
            "category": "Certificate of Analysis",
            "linked_to": "ITM-001 / LOT-002 / MTH241015-B",
            "file_name": "COA-MRK-241015.pdf",
            "uploaded_by": "Warehouse Officer",
            "uploaded_at": "2024-10-15 09:12",
            "expiry": "—",
            "status": "Active",
        },
        {
            "id": "DOC-002",
            "doc_no": "SDS-MTH-2024",
            "title": "Methanol Safety Data Sheet",
            "category": "Safety Data Sheet",
            "linked_to": "ITM-001",
            "file_name": "SDS-MTH-2024-v3.pdf",
            "uploaded_by": "Dr. Sarah Chen",
            "uploaded_at": "2024-01-08 11:24",
            "expiry": "2027-01-08",
            "status": "Active",
        },
        {
            "id": "DOC-003",
            "doc_no": "COA-USP-2024-05",
            "title": "Paracetamol Reference Standard COA",
            "category": "Certificate of Analysis",
            "linked_to": "ITM-003 / LOT-004 / PAR-USP-2024-05",
            "file_name": "COA-USP-PAR-240515.pdf",
            "uploaded_by": "QC Manager",
            "uploaded_at": "2024-05-15 14:01",
            "expiry": "—",
            "status": "Active",
        },
        {
            "id": "DOC-004",
            "doc_no": "INV-2024-0451",
            "title": "PO 0451 Vendor Invoice",
            "category": "Invoice",
            "linked_to": "GR-2024-3301",
            "file_name": "INV-MRK-0451.pdf",
            "uploaded_by": "Warehouse Officer",
            "uploaded_at": "2024-10-15 09:18",
            "expiry": "—",
            "status": "Active",
        },
        {
            "id": "DOC-005",
            "doc_no": "SDS-NAOH-2024",
            "title": "Sodium Hydroxide SDS",
            "category": "Safety Data Sheet",
            "linked_to": "ITM-008",
            "file_name": "SDS-NAOH-2024.pdf",
            "uploaded_by": "Dr. Sarah Chen",
            "uploaded_at": "2024-02-19 10:00",
            "expiry": "2027-02-19",
            "status": "Active",
        },
        {
            "id": "DOC-006",
            "doc_no": "AUDIT-MRK-2024",
            "title": "Merck Vendor Audit Report 2024",
            "category": "Vendor Audit",
            "linked_to": "VND-001",
            "file_name": "Audit-Merck-2024.pdf",
            "uploaded_by": "Auditor",
            "uploaded_at": "2024-03-15 16:42",
            "expiry": "2025-03-15",
            "status": "Active",
        },
    ]

    document_categories: list[DocumentCategory] = [
        {
            "id": "DC-001",
            "name": "Certificate of Analysis",
            "description": "Vendor-provided lot release certificate",
            "retention_days": 1825,
            "required_for": "Receiving",
        },
        {
            "id": "DC-002",
            "name": "Safety Data Sheet",
            "description": "Hazard communication document, refreshed every 3 years",
            "retention_days": 3650,
            "required_for": "Hazardous Items",
        },
        {
            "id": "DC-003",
            "name": "Invoice",
            "description": "Vendor invoice for receivings",
            "retention_days": 2555,
            "required_for": "Receiving",
        },
        {
            "id": "DC-004",
            "name": "Vendor Audit",
            "description": "On-site or remote vendor qualification audit",
            "retention_days": 1825,
            "required_for": "Vendor Qualification",
        },
        {
            "id": "DC-005",
            "name": "Internal Prep Log",
            "description": "Internal preparation and standardization records",
            "retention_days": 1825,
            "required_for": "Internal Prep",
        },
        {
            "id": "DC-006",
            "name": "NAPZA Registry",
            "description": "Controlled substances ledger and registry forms",
            "retention_days": 3650,
            "required_for": "NAPZA Items",
        },
    ]

    expiry_tasks: list[ExpiryTask] = [
        {
            "id": "EXP-001",
            "task_no": "EXP-2024-001",
            "item_name": "Phosphate Buffer pH 6.8",
            "lot_number": "PHB-INT-241101",
            "expiry_date": "2024-12-01",
            "days_to_expiry": 13,
            "assigned_to": "Warehouse Officer",
            "status": "Open",
            "action": "Re-prepare or quarantine",
            "completed_at": "",
        },
        {
            "id": "EXP-002",
            "task_no": "EXP-2024-002",
            "item_name": "Acetonitrile HPLC Grade",
            "lot_number": "ACE240920-A",
            "expiry_date": "2025-03-20",
            "days_to_expiry": 122,
            "assigned_to": "QC Analyst",
            "status": "In Progress",
            "action": "Plan reorder cycle",
            "completed_at": "",
        },
        {
            "id": "EXP-003",
            "task_no": "EXP-2024-003",
            "item_name": "Morphine Sulfate Standard",
            "lot_number": "MOR-USP-2024-02",
            "expiry_date": "2025-02-10",
            "days_to_expiry": 84,
            "assigned_to": "QC Manager",
            "status": "Open",
            "action": "NAPZA disposal pre-check",
            "completed_at": "",
        },
        {
            "id": "EXP-004",
            "task_no": "EXP-2024-004",
            "item_name": "Paracetamol Reference Standard",
            "lot_number": "PAR-USP-2024-05",
            "expiry_date": "2025-05-15",
            "days_to_expiry": 178,
            "assigned_to": "QC Analyst",
            "status": "Completed",
            "action": "Reorder placed",
            "completed_at": "2024-11-10",
        },
    ]

    transfers: list[Transfer] = [
        {
            "id": "TRF-001",
            "transfer_no": "TRF-2024-0501",
            "item_name": "Methanol HPLC Grade",
            "lot_number": "MTH240801-A",
            "quantity": 5.0,
            "unit": "L",
            "from_location": "Solvent Cabinet A",
            "to_location": "Lab Bench 3",
            "requested_by": "John Martinez",
            "approved_by": "Dr. Sarah Chen",
            "status": "Completed",
            "created_at": "2024-11-10 09:00",
            "completed_at": "2024-11-10 09:35",
            "reason": "Method development workspace",
        },
        {
            "id": "TRF-002",
            "transfer_no": "TRF-2024-0502",
            "item_name": "Volumetric Flask 100mL Class A",
            "lot_number": "—",
            "quantity": 4.0,
            "unit": "pcs",
            "from_location": "Glassware Cabinet C",
            "to_location": "Wet Chemistry Lab",
            "requested_by": "Akira Tanaka",
            "approved_by": "",
            "status": "Pending",
            "created_at": "2024-11-13 11:30",
            "completed_at": "",
            "reason": "Routine stock replenishment",
        },
    ]

    notifications: list[Notification] = [
        {
            "id": "NTF-001",
            "timestamp": "2024-11-13 08:50",
            "severity": "high",
            "title": "NAPZA Request Pending",
            "message": "Emily Rodriguez requested 50 mg morphine sulfate. NAPZA registry approval required.",
            "target_role": "QC Manager",
            "read": False,
        },
        {
            "id": "NTF-002",
            "timestamp": "2024-11-13 07:30",
            "severity": "medium",
            "title": "Buffer expiring in 13 days",
            "message": "Phosphate Buffer pH 6.8 (PHB-INT-241101) expires 2024-12-01.",
            "target_role": "QC Admin",
            "read": False,
        },
        {
            "id": "NTF-003",
            "timestamp": "2024-11-12 11:08",
            "severity": "medium",
            "title": "High priority MR",
            "message": "Methanol request MR-2024-1102 awaiting approval.",
            "target_role": "QC Manager",
            "read": False,
        },
        {
            "id": "NTF-004",
            "timestamp": "2024-11-12 09:00",
            "severity": "low",
            "title": "Stock low: Acetonitrile",
            "message": "Acetonitrile HPLC Grade is below minimum (12.0 L / 15.0 L).",
            "target_role": "QC Admin",
            "read": True,
        },
        {
            "id": "NTF-005",
            "timestamp": "2024-11-11 16:22",
            "severity": "high",
            "title": "Out of stock",
            "message": "Caffeine Reference Standard at 0 g; reorder pending.",
            "target_role": "QC Manager",
            "read": True,
        },
    ]

    md_requests: list[MasterDataRequest] = [
        {
            "id": "MDR-001",
            "request_no": "MDR-2024-0011",
            "entity": "Item",
            "target": "ITM-002 Acetonitrile",
            "change_type": "Update Min Level",
            "proposed_value": "20.0 L (was 15.0 L)",
            "requester": "John Martinez",
            "approver": "",
            "status": "Pending Approval",
            "created_at": "2024-11-12 14:00",
            "rationale": "Increased throughput in HPLC method dev",
        },
        {
            "id": "MDR-002",
            "request_no": "MDR-2024-0012",
            "entity": "Vendor",
            "target": "VND-007 Acme Reagents",
            "change_type": "Reactivate",
            "proposed_value": "Status: Active",
            "requester": "QC Admin",
            "approver": "Dr. Sarah Chen",
            "status": "Approved",
            "created_at": "2024-11-08 10:11",
            "rationale": "Re-qualified after corrective audit",
        },
    ]

    settings: list[SystemSetting] = [
        {
            "key": "fefo_strict",
            "label": "Strict FEFO enforcement",
            "value": "On",
            "category": "Inventory",
            "description": "Issue must use earliest-expiry lot unless override reason provided",
        },
        {
            "key": "negative_stock",
            "label": "Allow negative stock",
            "value": "Off",
            "category": "Inventory",
            "description": "Service layer rejects any operation that would result in negative on-hand",
        },
        {
            "key": "self_approval",
            "label": "Allow self-approval",
            "value": "Off",
            "category": "Governance",
            "description": "Submitter cannot approve their own request or adjustment",
        },
        {
            "key": "expiry_alert_days",
            "label": "Expiry alert window",
            "value": "90 days",
            "category": "Notifications",
            "description": "Lot is flagged as expiring soon when days-to-expiry ≤ this value",
        },
        {
            "key": "default_release_status",
            "label": "Default lot status on receiving",
            "value": "Pending Release",
            "category": "Receiving",
            "description": "Newly received lots require QC release before becoming available",
        },
        {
            "key": "napza_dual_signoff",
            "label": "NAPZA dual sign-off",
            "value": "Required",
            "category": "Governance",
            "description": "NAPZA issue and adjustment require two approvals",
        },
        {
            "key": "audit_immutability",
            "label": "Audit ledger immutability",
            "value": "Enforced",
            "category": "Governance",
            "description": "Audit log entries are append-only; never edited or deleted",
        },
        {
            "key": "migration_lot_tag",
            "label": "Migration lot tag",
            "value": "MIG",
            "category": "Migration",
            "description": "Opening balances import lots with the MIG prefix and migration location",
        },
    ]

    new_vendor_name: str = ""
    new_vendor_code: str = ""
    new_vendor_category: str = "Reagent Manufacturer"
    new_vendor_contact: str = ""
    new_vendor_email: str = ""
    new_vendor_phone: str = ""

    notification_filter: str = "All"
    reset_confirm_text: str = ""

    @rx.var
    def active_vendor_count(self) -> int:
        return len([v for v in self.vendors if v["status"] == "Active"])

    @rx.var
    def suspended_vendor_count(self) -> int:
        return len([v for v in self.vendors if v["status"] == "Suspended"])

    @rx.var
    def open_expiry_tasks(self) -> int:
        return len([e for e in self.expiry_tasks if e["status"] != "Completed"])

    @rx.var
    def pending_transfer_count(self) -> int:
        return len([t for t in self.transfers if t["status"] == "Pending"])

    @rx.var
    def unread_notification_count(self) -> int:
        return len([n for n in self.notifications if not n["read"]])

    @rx.var
    def filtered_notifications(self) -> list[Notification]:
        if self.notification_filter == "All":
            return self.notifications
        if self.notification_filter == "Unread":
            return [n for n in self.notifications if not n["read"]]
        return [
            n
            for n in self.notifications
            if n["severity"] == self.notification_filter.lower()
        ]

    @rx.var
    def pending_md_count(self) -> int:
        return len(
            [m for m in self.md_requests if m["status"] == "Pending Approval"]
        )

    @rx.var
    async def visible_vendors(self) -> list[Vendor]:
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        return mask_vendor_list(self.vendors, auth.current_role)

    @rx.var
    async def can_manage_vendors(self) -> bool:
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        return can_edit_vendor(auth.current_role)

    @rx.event
    def set_new_vendor_name(self, v: str):
        self.new_vendor_name = v

    @rx.event
    def set_new_vendor_code(self, v: str):
        self.new_vendor_code = v

    @rx.event
    def set_new_vendor_category(self, v: str):
        self.new_vendor_category = v

    @rx.event
    def set_new_vendor_contact(self, v: str):
        self.new_vendor_contact = v

    @rx.event
    def set_new_vendor_email(self, v: str):
        self.new_vendor_email = v

    @rx.event
    def set_new_vendor_phone(self, v: str):
        self.new_vendor_phone = v

    @rx.event
    def set_notification_filter(self, v: str):
        self.notification_filter = v

    @rx.event
    def set_reset_confirm(self, v: str):
        self.reset_confirm_text = v

    @rx.event
    async def add_vendor(self):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        if not can_edit_vendor(auth.current_role):
            yield rx.toast.error(
                f"Role '{auth.current_role}' is not authorized to manage vendors."
            )
            return
        if not self.new_vendor_name.strip():
            yield rx.toast.error("Vendor name is required.")
            return
        if not self.new_vendor_code.strip():
            yield rx.toast.error("Vendor code is required.")
            return
        new_v: Vendor = {
            "id": f"VND-{uuid.uuid4().hex[:6].upper()}",
            "name": self.new_vendor_name,
            "code": self.new_vendor_code.upper(),
            "category": self.new_vendor_category,
            "contact_person": self.new_vendor_contact,
            "email": self.new_vendor_email,
            "phone": self.new_vendor_phone,
            "address": "—",
            "status": "Active",
            "qualified": False,
            "last_audit": "—",
            "notes": "Newly registered — pending qualification",
        }
        self.vendors.insert(0, new_v)
        self.new_vendor_name = ""
        self.new_vendor_code = ""
        self.new_vendor_contact = ""
        self.new_vendor_email = ""
        self.new_vendor_phone = ""
        yield rx.toast.success(f"Vendor {new_v['code']} added")

    @rx.event
    async def toggle_vendor_status(self, vendor_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        if not can_edit_vendor(auth.current_role):
            yield rx.toast.error("Not authorized to change vendor status.")
            return
        for v in self.vendors:
            if v["id"] == vendor_id:
                v["status"] = (
                    "Suspended" if v["status"] == "Active" else "Active"
                )
                yield rx.toast(f"{v['name']} → {v['status']}")
                return

    @rx.event
    def mark_notification_read(self, ntf_id: str):
        for n in self.notifications:
            if n["id"] == ntf_id:
                n["read"] = True
                return

    @rx.event
    def mark_all_read(self):
        for n in self.notifications:
            n["read"] = True
        yield rx.toast.success("All notifications marked as read")

    @rx.event
    def complete_expiry_task(self, task_id: str):
        for t in self.expiry_tasks:
            if t["id"] == task_id:
                t["status"] = "Completed"
                t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                yield rx.toast.success(f"Task {t['task_no']} completed")
                return

    @rx.event
    async def approve_transfer(self, trf_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        for t in self.transfers:
            if t["id"] == trf_id:
                if t["requested_by"] == auth.current_user:
                    yield rx.toast.error("Self-approval is not permitted.")
                    return
                t["status"] = "Completed"
                t["approved_by"] = auth.current_user
                t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                yield rx.toast.success(f"Transfer {t['transfer_no']} approved")
                return

    @rx.event
    async def approve_md_request(self, mdr_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        for m in self.md_requests:
            if m["id"] == mdr_id:
                if m["requester"] == auth.current_user:
                    yield rx.toast.error("Self-approval is not permitted.")
                    return
                m["status"] = "Approved"
                m["approver"] = auth.current_user
                yield rx.toast.success(f"{m['request_no']} approved")
                return

    @rx.event
    async def reject_md_request(self, mdr_id: str):
        from app.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        for m in self.md_requests:
            if m["id"] == mdr_id:
                if m["requester"] == auth.current_user:
                    yield rx.toast.error("Self-rejection is not permitted.")
                    return
                m["status"] = "Rejected"
                m["approver"] = auth.current_user
                yield rx.toast(f"{m['request_no']} rejected")
                return

    @rx.event
    async def perform_operational_reset(self):
        """Admin-only operational reset.

        Clears transactional data (requests, issues, receivings, adjustments,
        transfers, expiry tasks, notifications, audit log) but preserves
        accounts, roles, vendors, items, lots master, document categories,
        and system settings.
        """
        from app.states.auth_state import AuthState
        from app.states.operations_state import OperationsState
        from app.states.migration_state import MigrationState

        auth = await self.get_state(AuthState)
        ok, reason = can_perform_reset(
            auth.current_role, self.reset_confirm_text
        )
        if not ok:
            yield rx.toast.error(reason)
            return

        ops = await self.get_state(OperationsState)
        mig = await self.get_state(MigrationState)

        ops.requests = []
        ops.issues = []
        ops.receivings = []
        ops.adjustments = []
        ops.audit_log = []
        self.transfers = []
        self.expiry_tasks = []
        self.notifications = []
        self.md_requests = []
        mig.pending_rows = []

        ops._audit(
            auth.current_user,
            auth.current_role,
            "OPERATIONAL_RESET",
            "system",
            "Cleared transactional data; preserved accounts, roles, vendors, items, settings.",
        )

        self.reset_confirm_text = ""
        yield rx.toast.success(
            "Operational reset complete — accounts and roles preserved."
        )