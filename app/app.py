import reflex as rx
from app.components.layout import page_layout
from app.components.dashboard import dashboard_view
from app.components.inventory_view import inventory_view
from app.components.item_detail import item_detail_view
from app.components.lots_view import lots_view
from app.components.admin_view import admin_view
from app.components.material_requests_view import material_requests_view
from app.components.issue_view import issue_view
from app.components.receiving_view import receiving_view
from app.components.adjustments_view import adjustments_view
from app.components.vendors_view import vendors_view
from app.components.documents_view import documents_view
from app.components.expiry_view import expiry_view
from app.components.transfers_view import transfers_view
from app.components.reports_view import reports_view
from app.components.scan_view import scan_view
from app.components.labels_view import labels_view
from app.components.notifications_view import notifications_view
from app.components.migration_view import migration_view
from app.components.settings_view import settings_view
from app.states.inventory_state import InventoryState


def index() -> rx.Component:
    return page_layout(
        "Dashboard",
        "QC laboratory stock overview and operational alerts",
        dashboard_view(),
    )


def inventory_page() -> rx.Component:
    return page_layout(
        "Inventory",
        "Browse, search, and manage all stocked items in the QC laboratory",
        inventory_view(),
    )


def item_detail_page() -> rx.Component:
    return page_layout(
        "Item Detail",
        "Full information including stock balances, lots, and movement history",
        item_detail_view(),
    )


def lots_page() -> rx.Component:
    return page_layout(
        "Lots & Batches",
        "Track every received lot with expiry monitoring and FEFO ordering",
        lots_view(),
    )


def admin_page() -> rx.Component:
    return page_layout(
        "Admin & Roles",
        "Role-based permissions, system settings, and governance",
        admin_view(),
    )


def requests_page() -> rx.Component:
    return page_layout(
        "Material Requests",
        "Submit, review, and approve material requests with NAPZA and hazard governance",
        material_requests_view(),
    )


def issue_page() -> rx.Component:
    return page_layout(
        "Issue / Consume",
        "FEFO-driven lot selection with override capture and audit logging",
        issue_view(),
    )


def receiving_page() -> rx.Component:
    return page_layout(
        "Receiving",
        "Goods receipt with multi-lot support, document linkage, and pending-release defaults",
        receiving_view(),
    )


def adjustments_page() -> rx.Component:
    return page_layout(
        "Adjustments",
        "Submit and approve stock adjustments with self-approval protection and audit trail",
        adjustments_view(),
    )


def vendors_page() -> rx.Component:
    return page_layout(
        "Vendors & Sources",
        "Qualified supplier directory, contacts, and audit history",
        vendors_view(),
    )


def documents_page() -> rx.Component:
    return page_layout(
        "Documents",
        "Certificates, SDS, invoices, and audit reports linked to items, lots, and vendors",
        documents_view(),
    )


def expiry_page() -> rx.Component:
    return page_layout(
        "Expiry Check Tasks",
        "Track upcoming expirations and assign disposition actions",
        expiry_view(),
    )


def transfers_page() -> rx.Component:
    return page_layout(
        "Internal Transfers",
        "Move stock between lab locations with self-approval protection",
        transfers_view(),
    )


def reports_page() -> rx.Component:
    return page_layout(
        "Reports",
        "Operational metrics, stock-level rollups, and governance counters",
        reports_view(),
    )


def scan_page() -> rx.Component:
    return page_layout(
        "Scan & Lookup",
        "Scan barcodes, QR codes, or SKUs for fast item lookup",
        scan_view(),
    )


def labels_page() -> rx.Component:
    return page_layout(
        "Lot Labels",
        "Print or export QR-coded labels for every active lot",
        labels_view(),
    )


def notifications_page() -> rx.Component:
    return page_layout(
        "Notifications",
        "Role-targeted alerts for stock, expiry, governance, and approval events",
        notifications_view(),
    )


def migration_page() -> rx.Component:
    return page_layout(
        "Migration",
        "CSV import for opening balances with MIG lot tagging and Released status",
        migration_view(),
    )


def settings_page() -> rx.Component:
    return page_layout(
        "Settings & Governance",
        "System settings, master data change requests, audit trail, and operational reset",
        settings_view(),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(
    item_detail_page,
    route="/inventory/[item_id]",
    on_load=InventoryState.load_item_from_route,
)
app.add_page(inventory_page, route="/inventory")
app.add_page(lots_page, route="/lots")
app.add_page(admin_page, route="/admin")
app.add_page(requests_page, route="/requests")
app.add_page(issue_page, route="/issue")
app.add_page(receiving_page, route="/receiving")
app.add_page(adjustments_page, route="/adjustments")
app.add_page(vendors_page, route="/vendors")
app.add_page(documents_page, route="/documents")
app.add_page(expiry_page, route="/expiry")
app.add_page(transfers_page, route="/transfers")
app.add_page(reports_page, route="/reports")
app.add_page(scan_page, route="/scan")
app.add_page(labels_page, route="/labels")
app.add_page(notifications_page, route="/notifications")
app.add_page(migration_page, route="/migration")
app.add_page(settings_page, route="/settings")