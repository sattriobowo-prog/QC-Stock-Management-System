# QC Stock Management Persistent Database Foundation Phase

## Phase 1: Persistent Data Foundation and Seeds ✅
- [x] Convert the production persistence layer to Reflex-hosted database model patterns for security, reference, inventory, stock ledger, audit, migration, and workflow-ready entities.
- [x] Add idempotent seed routines for required roles, development profile, reference lookups, document types, FEFO override reasons, transaction types, system settings, and default migration location.
- [x] Preserve existing UI pages, navigation, and workflow scaffolds while shifting production data concepts away from in-memory lists.
- [x] Add GxP/CSV-readiness comments for migration evidence, transactions, audit trail, approvals, overrides, and admin reset actions.

## Phase 2: Service-Layer Integrity and Validation ✅
- [x] Enforce the exact four-role permission foundation through server-side services.
- [x] Centralize stock balance, stock transaction, audit logging, FEFO allocation, opening balance posting, migration validation, and admin reset planning services.
- [x] Validate CurrentStock, Active90, stock status labels, FEFO ordering, negative-stock rejection, and opening-balance posting rules.
- [x] Confirm durable migration tracking, stock ledger, audit, and reset foundations are ready for the next CSV migration phase.