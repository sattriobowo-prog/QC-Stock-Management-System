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
PO = PurchaseOrderSchema
PurchaseOrderLine = PurchaseOrderLineSchema
POLine = PurchaseOrderLineSchema
LotReceipt = LotReceiptSchema
Reservation = ReservationSchema
FefoOverride = FefoOverrideSchema

__all__ = [
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
    "PO",
    "PurchaseOrderLine",
    "POLine",
    "LotReceipt",
    "Reservation",
    "FefoOverride",
]