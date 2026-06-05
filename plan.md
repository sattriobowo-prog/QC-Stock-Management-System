# QC Stock Management Continuation Plan

## Phase 1: Persistent Foundation and Role Model ✅
- [x] Add database-backed models for core QC inventory, stock, requests, documents, migration, settings, notifications, and audit entities.
- [x] Seed required roles, lookup data, default migration location, document types, transaction types, settings, and representative operational data.
- [x] Replace the role model with exactly QC Analyst, QC Admin, QC Manager, and Admin, including server-side permission checks.
- [x] Add audit helper patterns and stock integrity service rules for immutable stock ledger entries and negative-stock rejection.
- [x] Preserve the existing clean UI direction with light sidebar, blue accent, compact tables, white bordered cards, and status badges.

## Phase 2: Database-Backed Inventory, Lots, Vendors, and Detail Views ✅
- [x] Refactor inventory, item detail, lots/batches, vendors/sources, stock balances, and transactions to read from persistent data.
- [x] Add database-backed search, filters, QC status badges, stock status calculations, and stock balance rollups.
- [x] Ensure item detail tabs show overview, sources, lots, stock, documents, and activity from persistent records.
- [x] Restrict sensitive vendor contact fields by role through service-level checks.
- [x] Keep existing navigation and page coverage intact while replacing unsafe demo-state patterns.

## Phase 3: Migration Readiness, Admin Protection, and Workflow Scaffolds ✅
- [x] Prepare migration screens and services for the required Access CSV files with dry-run validation, row errors, idempotency scaffolding, and Admin-only enforcement.
- [x] Protect Danger Zone Reset with Admin-only service checks and preserve accounts/roles during operational data reset scaffolding.
- [x] Scaffold database-backed material request, receiving, adjustment, document, label, report, notification, and scanner workflows without unsafe direct stock edits.
- [x] Add FEFO allocation and opening-balance migration service scaffolds with correct unknown-expiry and released-stock rules.
- [x] Validate core persistent events, role checks, migration preview behavior, and stock integrity rules.