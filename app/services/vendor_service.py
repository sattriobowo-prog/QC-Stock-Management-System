"""Server-side vendor data access with role-based field masking.

Sensitive vendor contact fields (email, phone, address, notes) are
restricted to roles holding `manage_vendors`. Other roles see masked
placeholders. Enforced at the service layer — UI-only conditionals
must NOT be relied on for confidentiality.
"""

from __future__ import annotations
from app.services.permissions import has_permission

SENSITIVE_FIELDS = ("email", "phone", "address", "notes", "contact_person")
MASK = "••• restricted •••"


def mask_vendor_for_role(vendor: dict, role: str) -> dict:
    """Return a vendor dict with sensitive fields masked unless role is allowed."""
    if has_permission(role, "manage_vendors"):
        return dict(vendor)
    masked = dict(vendor)
    for f in SENSITIVE_FIELDS:
        if f in masked and masked[f]:
            masked[f] = MASK
    return masked


def mask_vendor_list(vendors: list[dict], role: str) -> list[dict]:
    return [mask_vendor_for_role(v, role) for v in vendors]


def can_edit_vendor(role: str) -> bool:
    return has_permission(role, "manage_vendors")