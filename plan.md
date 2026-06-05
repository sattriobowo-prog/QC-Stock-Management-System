# QC Stock Management Persistent Foundation Phase

## Phase 1: Database and Stock Integrity Foundation ✅
- [x] Replace dataclass-only schema scaffolding with real persistent database model definitions for inventory, reference data, stock ledger, audit, migration tracking, and later workflow entities.
- [x] Add idempotent development seeding for required roles, lookup/reference data, migration location, document types, transaction types, system settings, and minimal safe sample records.
- [x] Align server-side permissions with the required four-role matrix and isolate the current role switcher as development-only behavior.
- [x] Centralize stock calculations, stock status priority, FEFO allocation, negative-stock rejection, and opening-balance stock posting rules.
- [x] Preserve the current page coverage and UI while making inventory, lots, vendors, balances, transactions, audit, admin, and migration foundations database-ready.

## Phase 2: Validation and Stabilization ✅
- [x] Validate required roles and permission constraints, especially that QC Analyst cannot issue stock.
- [x] Validate CurrentStock, Active90, stock status labels, FEFO ordering, and expired/unknown-expiry handling.
- [x] Validate opening-balance behavior for lot numbering, unknown expiry, migration location, stock balance updates, stock transaction creation, and audit logging.
- [x] Verify migration tracking model concepts and seed routines are ready for the next CSV migration phase.
- [x] Document known limitations for deferred workflows without implementing those workflows in this phase.