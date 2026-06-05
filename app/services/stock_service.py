"""Stock integrity service rules.

These helpers enforce the QC Stock Management invariants:
  * Negative stock is rejected without silent clamping.
  * FEFO (First-Expiry-First-Out) is the default lot selection rule.
  * Only Released, positive-quantity lots are eligible for issue.
"""

from __future__ import annotations
from typing import Iterable


def validate_stock_change(
    on_hand: float, delta: float, unit: str = ""
) -> tuple[bool, str, float]:
    """Reject any operation that would drive on_hand negative.

    Returns (ok, reason, projected_on_hand).
    Never silently clamps — caller must handle the rejection explicitly.
    """
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


def eligible_lots_for_issue(lots: Iterable[dict], item_id: str) -> list[dict]:
    """Filter lots to those eligible for issue: Released, positive qty, item match."""
    return [
        lot
        for lot in lots
        if lot.get("item_id") == item_id
        and lot.get("status") == "Released"
        and float(lot.get("quantity", 0)) > 0
    ]


def _get_expiry_key(l: dict) -> int:
    return l.get("days_to_expiry", 10**9)


def select_fefo_lot(lots: Iterable[dict]) -> dict | None:
    """Return the FEFO (earliest expiry) lot from a pre-filtered eligible set."""
    eligible = list(lots)
    if not eligible:
        return None
    eligible.sort(key=_get_expiry_key)
    return eligible[0]


def fefo_allocation(
    lots: Iterable[dict], item_id: str, quantity: float
) -> tuple[bool, str, list[tuple[dict, float]]]:
    """Scaffold for multi-lot FEFO allocation.

    Returns (ok, reason, allocations) where allocations is a list of
    (lot, qty_to_draw) tuples, draining earliest-expiring lots first.
    """
    if quantity <= 0:
        return (False, "Quantity must be positive.", [])
    eligible = sorted(
        eligible_lots_for_issue(lots, item_id),
        key=_get_expiry_key,
    )
    remaining = quantity
    allocations: list[tuple[dict, float]] = []
    for lot in eligible:
        if remaining <= 0:
            break
        avail = float(lot.get("quantity", 0))
        draw = min(avail, remaining)
        allocations.append((lot, draw))
        remaining = round(remaining - draw, 6)
    if remaining > 0:
        return (
            False,
            f"Insufficient Released stock to fulfill {quantity}. "
            f"Short by {remaining}.",
            [],
        )
    return (True, "OK", allocations)