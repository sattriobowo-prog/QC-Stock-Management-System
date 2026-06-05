# QC Stock Management Implementation Plan

## Phase 1: Foundation, Data Model, Permissions, and Core Inventory UI ✅
- [x] Establish the application foundation with a clean professional QC laboratory design direction: light sidebar, blue accent, white bordered cards on a gray background, compact tables, and clear status badges.
- [x] Create database-ready relational models covering inventory, lots, stock balances, documents, requests, adjustments, transactions, audit logs, users, roles, settings, and lookup data.
- [x] Add role-aware service-layer patterns for stock calculations, permissions, audit writing, seed data, and stock movement validation.
- [x] Build the main navigation shell and initial Dashboard, Inventory, Item Detail, Lots/Batches, and Admin role display screens.
- [x] Seed realistic starter data including roles, lookup values, vendors, items, lots, stock balances, and immutable opening balance ledger entries.

## Phase 2: Operational Workflows and Controlled Stock Actions ✅
- [x] Build Material Requests with request list, form, status flow scaffolding, NAPZA/hazard warnings, and reservation-oriented service hooks.
- [x] Build Issue/Consume with FEFO lot selection, released-stock filtering, override reason/comment capture, and stock-changing service patterns.
- [x] Build Receiving and PO Evidence/Purchasing screens with multi-lot receiving scaffolding, document linkage placeholders, and pending-release defaults.
- [x] Build Adjustments with submitter queue, approval queue, self-approval protection, and ledger/audit service hooks.
- [x] Add workflow notifications and status messaging across request, issue, receiving, and adjustment screens.

## Phase 3: Governance, Migration, Reporting, and Administration Completion ✅
- [x] Build Vendors & Sources CRUD, Documents, Expiry Check Tasks, Transfers, Reports, Scan, Labels, Notifications, Migration, and Danger Zone Reset screens.
- [x] Add CSV migration scaffolding for opening balances with the required migration lot, location, released status, and opening balance transaction rules.
- [x] Add governance screens for system settings, master data change requests, document categories, audit trail, and operational reset confirmation protected by role.
- [x] Complete responsive UI polish, empty states, filters, compact tables, badges, warnings, and English-only copy across all pages.
- [x] Validate that all stock-changing UI paths are routed through service-layer operations and reject negative stock without silent clamping.