"""Validation scaffolds for the 11 Access CSV migration files.

Each file is validated row-by-row in a dry-run pass. Idempotency keys
prevent duplicate rows from being committed twice. Admin-only commit is
enforced at the state layer via app.services.admin_service.
"""

from __future__ import annotations
from typing import Callable
import re


CSV_SPECS: dict[str, dict] = {
    "categories.csv": {
        "label": "Categories",
        "description": "Item categories (e.g. Solvent, Reagent, Reference Standard)",
        "required_columns": ["code", "name"],
        "optional_columns": ["description"],
        "idempotency_key": ["code"],
    },
    "forms.csv": {
        "label": "Forms",
        "description": "Physical forms (Liquid, Solid, Powder, Tablet, etc.)",
        "required_columns": ["code", "name"],
        "optional_columns": ["description"],
        "idempotency_key": ["code"],
    },
    "storage_conditions.csv": {
        "label": "Storage Conditions",
        "description": "Storage / handling conditions (Ambient, 2–8 °C, −20 °C, etc.)",
        "required_columns": ["code", "name"],
        "optional_columns": ["temperature_min", "temperature_max", "notes"],
        "idempotency_key": ["code"],
    },
    "toxicity_classes.csv": {
        "label": "Toxicity Classes",
        "description": "GHS / hazard toxicity classification",
        "required_columns": ["code", "name"],
        "optional_columns": ["ghs_category", "description"],
        "idempotency_key": ["code"],
    },
    "napza_classes.csv": {
        "label": "NAPZA Classes",
        "description": "Controlled-substance schedule classes",
        "required_columns": ["code", "name"],
        "optional_columns": ["schedule", "description"],
        "idempotency_key": ["code"],
    },
    "vendors.csv": {
        "label": "Vendors",
        "description": "Qualified suppliers and manufacturers",
        "required_columns": ["code", "name", "category"],
        "optional_columns": [
            "contact_person",
            "email",
            "phone",
            "address",
            "status",
            "qualified",
            "last_audit",
        ],
        "idempotency_key": ["code"],
    },
    "items.csv": {
        "label": "Items",
        "description": "Item master with SKU, legacy code, category, unit, min/max",
        "required_columns": ["sku", "name", "category", "unit"],
        "optional_columns": [
            "legacy_code",
            "description",
            "min_level",
            "max_level",
            "reorder_point",
            "safety_stock",
            "is_napza",
            "is_hazard",
            "form",
            "storage_condition",
            "toxicity_class",
            "napza_class",
            "default_location",
            "default_vendor",
        ],
        "idempotency_key": ["sku"],
    },
    "item_manufacturers.csv": {
        "label": "Item Manufacturers",
        "description": "Manufacturer assignments per item (many-to-many)",
        "required_columns": ["item_sku", "manufacturer_code"],
        "optional_columns": ["is_primary", "notes"],
        "idempotency_key": ["item_sku", "manufacturer_code"],
    },
    "item_sources.csv": {
        "label": "Item Sources",
        "description": "Vendor / source assignments per item",
        "required_columns": ["item_sku", "vendor_code"],
        "optional_columns": ["is_primary", "lead_time_days", "notes"],
        "idempotency_key": ["item_sku", "vendor_code"],
    },
    "locations.csv": {
        "label": "Locations",
        "description": "Storage locations (cabinets, shelves, vaults)",
        "required_columns": ["code", "name"],
        "optional_columns": ["description", "restricted"],
        "idempotency_key": ["code"],
    },
    "opening_balances.csv": {
        "label": "Opening Balances",
        "description": "Opening-balance lots (MIG-tagged, Released)",
        "required_columns": ["sku", "quantity"],
        "optional_columns": ["expiry", "lot_number", "location", "notes"],
        "idempotency_key": ["sku", "lot_number"],
    },
}


CSV_FILE_ORDER: list[str] = [
    "categories.csv",
    "forms.csv",
    "storage_conditions.csv",
    "toxicity_classes.csv",
    "napza_classes.csv",
    "locations.csv",
    "vendors.csv",
    "items.csv",
    "item_manufacturers.csv",
    "item_sources.csv",
    "opening_balances.csv",
]


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_required_columns(
    file_name: str, header: list[str]
) -> tuple[bool, str]:
    spec = CSV_SPECS.get(file_name)
    if spec is None:
        return (False, f"Unknown file: {file_name}")
    missing = [c for c in spec["required_columns"] if c not in header]
    if missing:
        return (False, f"Missing required columns: {', '.join(missing)}")
    return (True, "OK")


def validate_row(file_name: str, row: dict, row_no: int) -> list[str]:
    spec = CSV_SPECS.get(file_name)
    if spec is None:
        return [f"Unknown file: {file_name}"]
    errors: list[str] = []
    for col in spec["required_columns"]:
        if not (row.get(col) or "").strip():
            errors.append(f"Missing required '{col}'")

    if file_name == "opening_balances.csv":
        qty = (row.get("quantity") or "").strip()
        try:
            q = float(qty) if qty else 0.0
            if q < 0:
                errors.append("Negative opening balance not allowed")
        except ValueError:
            errors.append("Invalid quantity (not numeric)")
        exp = (row.get("expiry") or "").strip()
        if exp and exp not in ("—", "-", "None") and (not _DATE_RE.match(exp)):
            errors.append("Invalid expiry format (expected YYYY-MM-DD)")

    if file_name == "items.csv":
        for col in ("min_level", "max_level", "reorder_point", "safety_stock"):
            v = (row.get(col) or "").strip()
            if v:
                try:
                    float(v)
                except ValueError:
                    errors.append(f"Invalid numeric value for '{col}'")

    return errors


def build_idempotency_key(file_name: str, row: dict) -> str:
    spec = CSV_SPECS.get(file_name, {})
    key_cols = spec.get("idempotency_key", [])
    parts = [(row.get(c) or "").strip() for c in key_cols]
    return f"{file_name}::" + "|".join(parts)