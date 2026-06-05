"""Immutable audit ledger helpers.

Audit entries are append-only — never edited or deleted. The helpers here
build canonical entry payloads that any state class can prepend to its
audit log list (and that a future persistence layer can insert verbatim).
"""

from __future__ import annotations
from datetime import datetime
import uuid


def build_audit_entry(
    user: str,
    role: str,
    action: str,
    target: str,
    detail: str,
) -> dict:
    return {
        "id": f"AUD-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": user,
        "role": role,
        "action": action,
        "target": target,
        "detail": detail,
    }


def build_transaction_entry(
    transaction_type: str,
    item_id: str,
    lot_number: str,
    delta: float,
    unit: str,
    user: str,
    role: str,
    reference: str = "",
    notes: str = "",
) -> dict:
    """Immutable stock-movement ledger row (transaction journal)."""
    return {
        "id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_type": transaction_type,
        "item_id": item_id,
        "lot_number": lot_number,
        "delta": delta,
        "unit": unit,
        "user": user,
        "role": role,
        "reference": reference,
        "notes": notes,
    }