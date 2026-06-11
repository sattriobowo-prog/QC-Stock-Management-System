from app.models.constants import (
    REQUIRED_ROLES,
    TRANSACTION_TYPES,
    TRANSACTION_TYPE_OPENING_BALANCE,
    TRANSACTION_TYPE_RECEIVE,
    TRANSACTION_TYPE_ISSUE,
    TRANSACTION_TYPE_TRANSFER,
    TRANSACTION_TYPE_ADJUST,
    TRANSACTION_TYPE_DISPOSE,
    TRANSACTION_TYPE_QUARANTINE,
    TRANSACTION_TYPE_RELEASE,
    TRANSACTION_TYPE_REJECT,
    TRANSACTION_TYPE_RESERVATION,
    DOCUMENT_TYPES,
    DOCUMENT_TYPE_SDS,
    DOCUMENT_TYPE_MSDS,
    DOCUMENT_TYPE_COA,
    DOCUMENT_TYPE_PO_EVIDENCE,
    DOCUMENT_TYPE_DELIVERY_ORDER,
    DOCUMENT_TYPE_OTHER,
    FEFO_OVERRIDE_REASONS,
    LOT_STATUSES,
    LOT_STATUS_PENDING_RELEASE,
    LOT_STATUS_RELEASED,
    LOT_STATUS_QUARANTINE,
    LOT_STATUS_REJECTED,
    LOT_STATUS_EXPIRED,
    DEFAULT_MIGRATION_LOCATION_CODE,
    DEFAULT_MIGRATION_LOCATION_NAME,
    EXPIRY_WARNING_DAYS_DEFAULT,
    DEV_PROFILE_USER_ID,
    DEV_PROFILE_FULL_NAME,
    DEV_PROFILE_EMAIL,
    DEV_PROFILE_ROLE,
)
from app.models.schemas import (
    ItemSchema,
    LotSchema,
    LocationSchema,
    VendorSchema,
    DocumentSchema,
    DocumentCategorySchema,
    MaterialRequestSchema,
    IssueRecordSchema,
    ReceivingRecordSchema,
    AdjustmentSchema,
    TransferSchema,
    ExpiryTaskSchema,
    NotificationSchema,
    MasterDataRequestSchema,
    SystemSettingSchema,
    AuditEntrySchema,
    StockTransactionSchema,
    MigrationBatchSchema,
    MigrationRowSchema,
    UserSchema,
    RoleSchema,
    StockBalanceSchema,
    CategorySchema,
    FormSchema,
    StorageConditionSchema,
    ToxicityClassSchema,
    NapzaClassSchema,
    ItemManufacturerSchema,
    ItemSourceSchema,
    ProfileSchema,
    PurchaseOrderSchema,
    PurchaseOrderLineSchema,
    LotReceiptSchema,
    MaterialRequestLineSchema,
    ReservationSchema,
    PendingAdjustmentSchema,
    FefoOverrideSchema,
)

# Stable persistent-foundation model names. These are aliases for the
# dataclass schema definitions in app.models.schemas, exported under the
# canonical names used by the rest of the application (and by the
# validation suite). Keeping them as aliases preserves the existing
# *Schema compatibility exports while providing the foundation names
# (Item, Lot, Vendor, ...) that callers expect to import from
# `app.models` directly.
Item = ItemSchema
Lot = LotSchema
Location = LocationSchema
Vendor = VendorSchema
Document = DocumentSchema
DocumentCategory = DocumentCategorySchema
MaterialRequest = MaterialRequestSchema
MaterialRequestLine = MaterialRequestLineSchema
IssueRecord = IssueRecordSchema
ReceivingRecord = ReceivingRecordSchema
Adjustment = AdjustmentSchema
PendingAdjustment = PendingAdjustmentSchema
Transfer = TransferSchema
ExpiryTask = ExpiryTaskSchema
ExpiryCheckTask = ExpiryTaskSchema
Notification = NotificationSchema
MasterDataRequest = MasterDataRequestSchema
MasterDataChangeRequest = MasterDataRequestSchema
SystemSetting = SystemSettingSchema
AuditEntry = AuditEntrySchema
AuditLog = AuditEntrySchema
StockTransaction = StockTransactionSchema
MigrationBatch = MigrationBatchSchema
MigrationRow = MigrationRowSchema
MigrationImportRow = MigrationRowSchema
User = UserSchema
UserProfile = ProfileSchema
Profile = ProfileSchema
Role = RoleSchema
UserRole = RoleSchema
StockBalance = StockBalanceSchema
Category = CategorySchema
Form = FormSchema
StorageCondition = StorageConditionSchema
ToxicityClass = ToxicityClassSchema
NapzaClass = NapzaClassSchema
ItemManufacturer = ItemManufacturerSchema
ItemSource = ItemSourceSchema
PurchaseOrder = PurchaseOrderSchema
POEvidenceRecord = PurchaseOrderSchema
PO = PurchaseOrderSchema
PurchaseOrderLine = PurchaseOrderLineSchema
POLine = PurchaseOrderLineSchema
LotReceipt = LotReceiptSchema
Reservation = ReservationSchema
FefoOverride = FefoOverrideSchema

__all__ = [
    # Phase 1 persistent-foundation constants
    "REQUIRED_ROLES",
    "TRANSACTION_TYPES",
    "TRANSACTION_TYPE_OPENING_BALANCE",
    "TRANSACTION_TYPE_RECEIVE",
    "TRANSACTION_TYPE_ISSUE",
    "TRANSACTION_TYPE_TRANSFER",
    "TRANSACTION_TYPE_ADJUST",
    "TRANSACTION_TYPE_DISPOSE",
    "TRANSACTION_TYPE_QUARANTINE",
    "TRANSACTION_TYPE_RELEASE",
    "TRANSACTION_TYPE_REJECT",
    "TRANSACTION_TYPE_RESERVATION",
    "DOCUMENT_TYPES",
    "DOCUMENT_TYPE_SDS",
    "DOCUMENT_TYPE_MSDS",
    "DOCUMENT_TYPE_COA",
    "DOCUMENT_TYPE_PO_EVIDENCE",
    "DOCUMENT_TYPE_DELIVERY_ORDER",
    "DOCUMENT_TYPE_OTHER",
    "FEFO_OVERRIDE_REASONS",
    "LOT_STATUSES",
    "LOT_STATUS_PENDING_RELEASE",
    "LOT_STATUS_RELEASED",
    "LOT_STATUS_QUARANTINE",
    "LOT_STATUS_REJECTED",
    "LOT_STATUS_EXPIRED",
    "DEFAULT_MIGRATION_LOCATION_CODE",
    "DEFAULT_MIGRATION_LOCATION_NAME",
    "EXPIRY_WARNING_DAYS_DEFAULT",
    "DEV_PROFILE_USER_ID",
    "DEV_PROFILE_FULL_NAME",
    "DEV_PROFILE_EMAIL",
    "DEV_PROFILE_ROLE",
    # Compatibility schema aliases
    "ItemSchema",
    "LotSchema",
    "LocationSchema",
    "VendorSchema",
    "DocumentSchema",
    "DocumentCategorySchema",
    "MaterialRequestSchema",
    "IssueRecordSchema",
    "ReceivingRecordSchema",
    "AdjustmentSchema",
    "TransferSchema",
    "ExpiryTaskSchema",
    "NotificationSchema",
    "MasterDataRequestSchema",
    "SystemSettingSchema",
    "AuditEntrySchema",
    "StockTransactionSchema",
    "MigrationBatchSchema",
    "MigrationRowSchema",
    "UserSchema",
    "RoleSchema",
    "StockBalanceSchema",
    "CategorySchema",
    "FormSchema",
    "StorageConditionSchema",
    "ToxicityClassSchema",
    "NapzaClassSchema",
    "ItemManufacturerSchema",
    "ItemSourceSchema",
    "ProfileSchema",
    "PurchaseOrderSchema",
    "PurchaseOrderLineSchema",
    "LotReceiptSchema",
    "MaterialRequestLineSchema",
    "ReservationSchema",
    "PendingAdjustmentSchema",
    "FefoOverrideSchema",
    # Persistent foundation canonical names
    "Item",
    "Lot",
    "Location",
    "Vendor",
    "Document",
    "DocumentCategory",
    "MaterialRequest",
    "MaterialRequestLine",
    "IssueRecord",
    "ReceivingRecord",
    "Adjustment",
    "PendingAdjustment",
    "Transfer",
    "ExpiryTask",
    "ExpiryCheckTask",
    "Notification",
    "MasterDataRequest",
    "MasterDataChangeRequest",
    "SystemSetting",
    "AuditEntry",
    "AuditLog",
    "StockTransaction",
    "MigrationBatch",
    "MigrationRow",
    "MigrationImportRow",
    "User",
    "UserProfile",
    "Profile",
    "Role",
    "UserRole",
    "StockBalance",
    "Category",
    "Form",
    "StorageCondition",
    "ToxicityClass",
    "NapzaClass",
    "ItemManufacturer",
    "ItemSource",
    "PurchaseOrder",
    "POEvidenceRecord",
    "PO",
    "PurchaseOrderLine",
    "POLine",
    "LotReceipt",
    "Reservation",
    "FefoOverride",
]