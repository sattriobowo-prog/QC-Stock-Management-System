"""Database-ready schemas for QC Stock Management.

These dataclasses describe the persistent shape of every core entity
(items, lots, requests, documents, migration, audit, notifications,
settings, users, roles). They are intentionally framework-light so they
can be mapped 1:1 to a future PostgreSQL ORM (SQLModel/SQLAlchemy)
without churn in callers.

NOTE: We deliberately do NOT use rx.Model here — persistence and
migrations are handled by the deployment mechanism, not by the app.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RoleSchema:
    name: str
    permissions: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class UserSchema:
    id: str
    full_name: str
    email: str
    role: str
    active: bool = True
    created_at: str = ""


@dataclass
class LocationSchema:
    id: str
    code: str
    name: str
    description: str = ""
    restricted: bool = False


@dataclass
class VendorSchema:
    id: str
    code: str
    name: str
    category: str
    contact_person: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    status: str = "Active"
    qualified: bool = False
    last_audit: str = ""
    notes: str = ""


@dataclass
class ItemSchema:
    id: str
    sku: str
    legacy_code: str
    name: str
    description: str
    category: str
    unit: str
    on_hand: float = 0.0
    reserved: float = 0.0
    available: float = 0.0
    incoming: float = 0.0
    min_level: float = 0.0
    max_level: float = 0.0
    reorder_point: float = 0.0
    safety_stock: float = 0.0
    total_received: float = 0.0
    total_issued: float = 0.0
    last_received_date: str = ""
    last_issued_date: str = ""
    location: str = ""
    status: str = "Released"
    is_napza: bool = False
    is_hazard: bool = False
    vendor: str = ""
    last_updated: str = ""
    created_at: str = ""


@dataclass
class LotSchema:
    id: str
    item_id: str
    lot_number: str
    quantity: float
    unit: str
    received_date: str
    expiry_date: str
    status: str = "Pending Release"
    location: str = ""
    vendor: str = ""


@dataclass
class DocumentCategorySchema:
    id: str
    name: str
    description: str
    retention_days: int
    required_for: str


@dataclass
class DocumentSchema:
    id: str
    doc_no: str
    title: str
    category: str
    linked_to: str
    file_name: str
    uploaded_by: str
    uploaded_at: str
    expiry: str = ""
    status: str = "Active"


@dataclass
class MaterialRequestSchema:
    id: str
    request_no: str
    requester: str
    purpose: str
    item_id: str
    quantity: float
    unit: str
    is_napza: bool = False
    is_hazard: bool = False
    status: str = "Pending Approval"
    priority: str = "Normal"
    created_at: str = ""
    notes: str = ""


@dataclass
class IssueRecordSchema:
    id: str
    issue_no: str
    item_id: str
    lot_number: str
    quantity: float
    unit: str
    issued_to: str
    purpose: str
    issued_by: str
    issued_at: str
    override_reason: str = ""


@dataclass
class ReceivingRecordSchema:
    id: str
    receiving_no: str
    po_number: str
    vendor: str
    item_id: str
    lot_number: str
    quantity: float
    unit: str
    received_date: str
    expiry_date: str
    status: str = "Pending Release"
    document_ref: str = ""
    received_by: str = ""
    notes: str = ""


@dataclass
class AdjustmentSchema:
    id: str
    adjustment_no: str
    item_id: str
    delta: float
    unit: str
    reason: str
    submitter: str
    status: str = "Pending Approval"
    created_at: str = ""
    approver: str = ""
    approved_at: str = ""
    notes: str = ""


@dataclass
class TransferSchema:
    id: str
    transfer_no: str
    item_id: str
    lot_number: str
    quantity: float
    unit: str
    from_location: str
    to_location: str
    requested_by: str
    status: str = "Pending"
    approved_by: str = ""
    created_at: str = ""
    completed_at: str = ""
    reason: str = ""


@dataclass
class ExpiryTaskSchema:
    id: str
    task_no: str
    item_id: str
    lot_number: str
    expiry_date: str
    days_to_expiry: int
    assigned_to: str
    action: str
    status: str = "Open"
    completed_at: str = ""


@dataclass
class NotificationSchema:
    id: str
    timestamp: str
    severity: str
    title: str
    message: str
    target_role: str
    read: bool = False


@dataclass
class MasterDataRequestSchema:
    id: str
    request_no: str
    entity: str
    target: str
    change_type: str
    proposed_value: str
    requester: str
    rationale: str
    status: str = "Pending Approval"
    approver: str = ""
    created_at: str = ""


@dataclass
class SystemSettingSchema:
    key: str
    label: str
    value: str
    category: str
    description: str = ""


@dataclass
class AuditEntrySchema:
    id: str
    timestamp: str
    user: str
    role: str
    action: str
    target: str
    detail: str


@dataclass
class StockTransactionSchema:
    id: str
    timestamp: str
    transaction_type: str
    item_id: str
    lot_number: str
    delta: float
    unit: str
    user: str
    role: str
    reference: str = ""
    notes: str = ""


@dataclass
class MigrationRowSchema:
    row_no: int
    sku: str
    item_name: str
    quantity: float
    unit: str
    expiry: str
    location: str
    lot_number: str
    status: str = "Released"
    error: str = ""


@dataclass
class MigrationBatchSchema:
    id: str
    batch_no: str
    file_name: str
    rows_total: int
    rows_valid: int
    rows_invalid: int
    rows_imported: int
    submitted_by: str
    submitted_at: str
    status: str = "Pending"