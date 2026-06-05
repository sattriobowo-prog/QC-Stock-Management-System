"""Stock balance rollup helpers (item / lot / location) and stock-status priority.

QC service-layer rules (Phase 1 — exact spec):

  * `current_stock` = sum of Released, non-expired lot quantities for an
    item. Includes lots with unknown expiry (`expiry_known=False`).
    Excludes Expired, Rejected, Quarantine, and Pending Release lots.

  * `active_90` = sum of Released lot quantities that are usable beyond
    today + 90 days. A lot contributes to Active90 ONLY when
    `expiry_known=True` AND `expiry_date > today + 90 days`. Unknown
    expiry lots are EXCLUDED from Active90 (cannot guarantee 90-day life).

  * Stock-status labels (exact strings — no "Critical", no "OK", no "Hold"):
        "Out of Stock"      — current_stock <= 0
        "Out of Stock Risk" — active_90 <= 0 (current still positive)
        "Low Stock"         — current_stock < min_level (or reorder_point)
        "Low Stock Risk"    — active_90 < min_level (or reorder_point)
        "Active"            — sufficient stock now and beyond 90 days
"""

from __future__ import annotations
from collections import defaultdict


_EXCLUDED_LOT_STATUSES = {
    "Expired",
    "Rejected",
    "Quarantine",
    "Pending Release",
}


def _resolve_metrics(
    item: dict, lots: list[dict] | None
) -> tuple[float, float]:
    cs = item.get("current_stock")
    a90 = item.get("active_90")
    if cs is None and lots is not None:
        cs = current_stock(lots, item.get("id", ""))
    if a90 is None and lots is not None:
        a90 = active_90_stock(lots, item.get("id", ""))
    if cs is None:
        cs = float(item.get("on_hand", 0))
    if a90 is None:
        a90 = 0.0
    return float(cs), float(a90)


def _threshold(item: dict) -> float:
    """Reorder point if set, else min_level."""
    rp = float(item.get("reorder_point", 0) or 0)
    if rp > 0:
        return rp
    return float(item.get("min_level", 0) or 0)


def stock_status_priority(item: dict, lots: list[dict] | None = None) -> int:
    """Lower priority value = more urgent. Used for sorting only."""
    cs, a90 = _resolve_metrics(item, lots)
    threshold = _threshold(item)
    if cs <= 0:
        return 1  # Out of Stock
    if a90 <= 0:
        return 2  # Out of Stock Risk
    if cs < threshold:
        return 3  # Low Stock
    if a90 < threshold:
        return 4  # Low Stock Risk
    return 5  # Active


def stock_status_label(item: dict, lots: list[dict] | None = None) -> str:
    p = stock_status_priority(item, lots)
    return {
        1: "Out of Stock",
        2: "Out of Stock Risk",
        3: "Low Stock",
        4: "Low Stock Risk",
        5: "Active",
    }.get(p, "Active")


def _is_expired(lot: dict) -> bool:
    """Lot is expired only when expiry_known AND days_to_expiry < 0."""
    if not _is_expiry_known(lot):
        return False
    return int(lot.get("days_to_expiry", 0)) < 0


def current_stock(lots: list[dict], item_id: str) -> float:
    """Released non-expired stock; includes unknown-expiry lots.

    Excludes lots in Expired, Rejected, Quarantine, Pending Release.
    """
    total = 0.0
    for l in lots:
        if l.get("item_id") != item_id:
            continue
        status = l.get("status", "")
        if status != "Released":
            continue
        if status in _EXCLUDED_LOT_STATUSES:
            continue
        if _is_expired(l):
            continue
        total += float(l.get("quantity", 0))
    return round(total, 4)


def _is_expiry_known(lot: dict) -> bool:
    """Known expiry: expiry_known explicitly True, or legacy non-empty
    expiry_date string."""
    if "expiry_known" in lot:
        return bool(lot.get("expiry_known"))
    exp = lot.get("expiry_date")
    return isinstance(exp, str) and exp.strip() not in ("", "—", "-", "None")


def active_90_stock(lots: list[dict], item_id: str) -> float:
    """Released stock with KNOWN expiry strictly beyond today + 90 days.

    Excludes unknown-expiry lots (cannot guarantee 90-day life) and any
    lot at or within the 90-day window, expired, or in restricted status.
    """
    total = 0.0
    for l in lots:
        if l.get("item_id") != item_id:
            continue
        if l.get("status") != "Released":
            continue
        if not _is_expiry_known(l):
            continue
        if _is_expired(l):
            continue
        if int(l.get("days_to_expiry", 0)) <= 90:
            continue
        total += float(l.get("quantity", 0))
    return round(total, 4)


def rollup_by_item_lot_location(lots: list[dict]) -> list[dict]:
    """Group lots into (item_id, lot_number, location) balances."""
    buckets: dict[tuple, dict] = {}
    for l in lots:
        key = (l.get("item_id"), l.get("lot_number"), l.get("location"))
        if key not in buckets:
            buckets[key] = {
                "item_id": l.get("item_id"),
                "item_name": l.get("item_name"),
                "lot_number": l.get("lot_number"),
                "location": l.get("location"),
                "quantity": 0.0,
                "unit": l.get("unit"),
                "status": l.get("status"),
                "expiry_date": l.get("expiry_date"),
                "days_to_expiry": l.get("days_to_expiry"),
                "vendor": l.get("vendor"),
            }
        buckets[key]["quantity"] = round(
            buckets[key]["quantity"] + float(l.get("quantity", 0)), 4
        )
    return list(buckets.values())


def rollup_by_location(lots: list[dict]) -> list[dict]:
    agg: dict[str, dict] = defaultdict(
        lambda: {"location": "", "lots": 0, "quantity": 0.0, "items": set()}
    )
    for l in lots:
        loc = l.get("location") or "UNASSIGNED"
        agg[loc]["location"] = loc
        agg[loc]["lots"] += 1
        agg[loc]["quantity"] = round(
            agg[loc]["quantity"] + float(l.get("quantity", 0)), 4
        )
        agg[loc]["items"].add(l.get("item_id"))
    return [
        {
            "location": v["location"],
            "lots": v["lots"],
            "quantity": v["quantity"],
            "item_count": len(v["items"]),
        }
        for v in agg.values()
    ]