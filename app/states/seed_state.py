"""Seed lookup data for QC Stock Management.

Provides the canonical lists of locations (including the default
MIGRATION holding area and UNASSIGNED), document categories,
transaction types, and system settings used across the app.
"""

import reflex as rx
from typing import TypedDict


class LocationLookup(TypedDict):
    code: str
    name: str
    description: str
    restricted: bool


class TransactionTypeLookup(TypedDict):
    code: str
    name: str
    direction: str
    description: str


class SystemSettingLookup(TypedDict):
    key: str
    label: str
    value: str
    category: str
    description: str


class SeedState(rx.State):
    locations: list[LocationLookup] = [
        {
            "code": "UNASSIGNED",
            "name": "UNASSIGNED",
            "description": "Default placeholder for items without a confirmed home location",
            "restricted": False,
        },
        {
            "code": "MIGRATION",
            "name": "Migration Holding Area",
            "description": "Default landing zone for opening-balance migration batches",
            "restricted": False,
        },
        {
            "code": "SOLV-A",
            "name": "Solvent Cabinet A",
            "description": "Flammable solvents — vented cabinet",
            "restricted": False,
        },
        {
            "code": "RGT-D",
            "name": "Reagent Shelf D",
            "description": "General reagents",
            "restricted": False,
        },
        {
            "code": "BUF-B",
            "name": "Buffer Shelf B",
            "description": "Prepared buffer solutions",
            "restricted": False,
        },
        {
            "code": "GLW-C",
            "name": "Glassware Cabinet C",
            "description": "Class A volumetric and graduated glassware",
            "restricted": False,
        },
        {
            "code": "CON-E",
            "name": "Consumable Shelf E",
            "description": "Filters, vials, single-use consumables",
            "restricted": False,
        },
        {
            "code": "CLD-R1",
            "name": "Cold Storage R-1",
            "description": "2–8 °C reference standards",
            "restricted": False,
        },
        {
            "code": "VLT-NPZ",
            "name": "Vault NPZ-01",
            "description": "Restricted NAPZA controlled-substance vault",
            "restricted": True,
        },
    ]

    transaction_types: list[TransactionTypeLookup] = [
        {
            "code": "OPENING_BALANCE",
            "name": "Opening Balance",
            "direction": "+",
            "description": "Migration credit posted as Released",
        },
        {
            "code": "RECEIVING",
            "name": "Receiving",
            "direction": "+",
            "description": "Goods receipt — defaults to Pending Release",
        },
        {
            "code": "RECEIVING_RELEASED",
            "name": "Receiving Released",
            "direction": "+",
            "description": "QC release moves a lot into available stock",
        },
        {
            "code": "ISSUE",
            "name": "Issue / Consume",
            "direction": "−",
            "description": "FEFO-driven consumption against a Released lot",
        },
        {
            "code": "ADJUSTMENT",
            "name": "Adjustment",
            "direction": "±",
            "description": "Approved positive or negative correction",
        },
        {
            "code": "TRANSFER",
            "name": "Internal Transfer",
            "direction": "0",
            "description": "Move stock between locations (no net change)",
        },
        {
            "code": "DISPOSAL",
            "name": "Disposal",
            "direction": "−",
            "description": "Expired or quarantined lot disposal",
        },
        {
            "code": "QUARANTINE",
            "name": "Quarantine",
            "direction": "0",
            "description": "Lot status change to Quarantine — blocks issue",
        },
    ]

    document_categories: list[dict[str, str]] = [
        {
            "name": "Certificate of Analysis",
            "description": "Vendor-provided lot release certificate",
            "required_for": "Receiving",
        },
        {
            "name": "Safety Data Sheet",
            "description": "Hazard communication document, refreshed every 3 years",
            "required_for": "Hazardous Items",
        },
        {
            "name": "Invoice",
            "description": "Vendor invoice for receivings",
            "required_for": "Receiving",
        },
        {
            "name": "Vendor Audit",
            "description": "On-site or remote vendor qualification audit",
            "required_for": "Vendor Qualification",
        },
        {
            "name": "Internal Prep Log",
            "description": "Internal preparation and standardization records",
            "required_for": "Internal Prep",
        },
        {
            "name": "NAPZA Registry",
            "description": "Controlled substances ledger and registry forms",
            "required_for": "NAPZA Items",
        },
    ]

    system_settings: list[SystemSettingLookup] = [
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
            "description": "Opening balances import lots with the MIG prefix",
        },
        {
            "key": "migration_holding_location",
            "label": "Migration holding location",
            "value": "Migration Holding Area",
            "category": "Migration",
            "description": "Default location for migrated opening-balance lots",
        },
        {
            "key": "default_unassigned_location",
            "label": "Default unassigned location",
            "value": "UNASSIGNED",
            "category": "Inventory",
            "description": "Placeholder location for items without a confirmed home",
        },
    ]