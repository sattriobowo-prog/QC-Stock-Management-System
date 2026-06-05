"""Stock integrity service rules (Phase 1 — exact spec).

Invariants enforced here:
  * Negative stock is REJECTED without silent clamping.
  * FEFO uses Released, non-expired lots only.
  * Sort: known expiry earliest-first; unknown-expiry lots come AFTER all
    dated lots (sentinel days_to_expiry = 10**9).
  * Multi-lot allocation supported; insufficient stock is rejected.
  * FEFO override is a placeholder requiring a reason/comment and
    triggers an audit log entry at the caller layer.
"""

from __future__ import annotations
from typing import Iterable


UNKNOWN_EXPIRY_SENTINEL = 10**9


def validate_stock_change(
    on_hand: float, delta: float, unit: str = ""
) -> tuple[bool, str, float]:
    projected = round(on_hand + delta, 6)
    if projected < 0:
        return (
            False,
            (
                f"Operation rejected: would result in negative stock "
                f"({projected:.3f} {unit}). Stock cannot go below zero."
            ),
            projected,
        )
    return (True, "OK", projected)


def _is_expired(lot: dict) -> bool:
    if not lot.get("expiry_known", True):
        return False
    return int(lot.get("days_to_expiry", 0)) < 0


def eligible_lots_for_issue(lots: Iterable[dict], item_id: str) -> list[dict]:
    """Released, positive-qty, non-expired lots for this item, FEFO-ordered.

    Sort order: known-expiry dated lots first by earliest days_to_expiry asc,
    then unknown-expiry lots after all dated non-expired lots.
    Excludes Pending Release, Quarantine, Rejected, and expired lots.
    """
    out: list[dict] = []
    for lot in lots:
        if lot.get("item_id") != item_id:
            continue
        if lot.get("status") != "Released":
            continue
        if float(lot.get("quantity", 0)) <= 0:
            continue
        if _is_expired(lot):
            continue
        out.append(lot)
    out.sort(key=_fefo_sort_key)
    return out


def _fefo_sort_key(l: dict) -> tuple[int, int]:
    """FEFO ordering: known-expiry first (sorted by days_to_expiry asc),
    unknown-expiry last (sentinel). Returns (group, days) where group=0
    for known and group=1 for unknown."""
    if l.get("expiry_known", True):
        return (0, int(l.get("days_to_expiry", 0)))
    return (1, UNKNOWN_EXPIRY_SENTINEL)


def select_fefo_lot(lots: Iterable[dict]) -> dict | None:
    eligible = list(lots)
    if not eligible:
        return None
    eligible.sort(key=_fefo_sort_key)
    return eligible[0]


def fefo_allocation(
    lots: Iterable[dict], item_id: str, quantity: float
) -> tuple[bool, str, list[tuple[dict, float]]]:
    """Multi-lot FEFO allocation.

    Returns (ok, reason, allocations) with each allocation as
    (lot, qty_to_draw). Drains earliest-expiring known lots first;
    unknown-expiry lots are used only after dated lots are exhausted.
    """
    if quantity <= 0:
        return (False, "Quantity must be positive.", [])
    eligible = sorted(
        eligible_lots_for_issue(lots, item_id),
        key=_fefo_sort_key,
    )
    remaining = quantity
    allocations: list[tuple[dict, float]] = []
    for lot in eligible:
        if remaining <= 0:
            break
        avail = float(lot.get("quantity", 0))
        if avail <= 0:
            continue
        draw = min(avail, remaining)
        allocations.append((lot, draw))
        remaining = round(remaining - draw, 6)
    if remaining > 0:
        return (
            False,
            (
                f"Insufficient Released stock to fulfill {quantity}. "
                f"Short by {remaining}."
            ),
            [],
        )
    return (True, "OK", allocations)


def validate_fefo_override(
    chosen_lot: dict,
    fefo_lot: dict,
    reason: str,
    comment: str = "",
) -> tuple[bool, str]:
    """Placeholder FEFO override validation.

    Override is permitted only with a non-empty reason. The caller is
    responsible for writing the audit log entry referencing both the
    chosen lot and the bypassed FEFO lot.
    """
    if chosen_lot.get("lot_number") == fefo_lot.get("lot_number"):
        return (True, "No override — FEFO lot selected.")
    if not reason or not reason.strip():
        return (
            False,
            "FEFO override rejected: reason is required when bypassing the "
            "earliest-expiry lot.",
        )
    return (True, "OK")