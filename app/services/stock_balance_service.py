"""Stock balance rollup helpers (item / lot / location) and stock-status priority.

QC service-layer rules:
  * `current_stock` = sum of Released-lot quantities for an item.
  * `active_90` = sum of Released-lot quantities that are usable beyond
    the 90-day expiry window. A lot contributes to Active90 ONLY when
    `expiry_known` is True AND `expiry_date > today + 90 days` (i.e.
    `days_to_expiry > 90`). Lots with unknown expiry and lots at or
    within the 90-day window are excluded.
  * Stock-status priority (lower = more urgent), evaluated against
    CurrentStock and Active90 vs the reorder point and safety stock:
        1 = Out of Stock      (CurrentStock <= 0)
        2 = Critical          (CurrentStock <= safety_stock)
        3 = Low               (Active90 < reorder_point  OR  CurrentStock < min_level)
        4 = OK
        5 = Hold              (Pending Release / Quarantine — informational)
"""

from __future__ import annotations
from collections import defaultdict


def _resolve_metrics(
    item: dict, lots: list[dict] | None
) -> tuple[float, float]:
    """Return (current_stock, active_90) — prefer values pre-attached to the
    item dict (as items_with_metrics does); otherwise compute from `lots`."""
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


def stock_status_priority(item: dict, lots: list[dict] | None = None) -> int:
    cs, a90 = _resolve_metrics(item, lots)
    safety = float(item.get("safety_stock", 0))
    reorder = float(item.get("reorder_point", 0))
    min_level = float(item.get("min_level", 0))
    status = item.get("status", "")
    if cs <= 0:
        return 1
    if cs <= safety:
        return 2
    if a90 < reorder or cs < min_level:
        return 3
    if status in ("Pending Release", "Quarantine"):
        return 5
    return 4


def stock_status_label(item: dict, lots: list[dict] | None = None) -> str:
    p = stock_status_priority(item, lots)
    return {
        1: "Out of Stock",
        2: "Critical",
        3: "Low",
        4: "OK",
        5: "Hold",
    }.get(p, "OK")


def current_stock(lots: list[dict], item_id: str) -> float:
    return round(
        sum(
            float(l.get("quantity", 0))
            for l in lots
            if l.get("item_id") == item_id and l.get("status") == "Released"
        ),
        4,
    )


def _is_expiry_known(lot: dict) -> bool:
    """A lot has a known expiry when expiry_known is explicitly True, or
    when expiry_date is a non-empty string (back-compat for legacy seed
    lots that pre-date the expiry_known field)."""
    if "expiry_known" in lot:
        return bool(lot.get("expiry_known"))
    exp = lot.get("expiry_date")
    return isinstance(exp, str) and exp.strip() not in ("", "—", "-", "None")


def active_90_stock(lots: list[dict], item_id: str) -> float:
    """Released stock with expiry strictly beyond today + 90 days.

    Excludes unknown-expiry lots and lots at or within the 90-day window.
    """
    total = 0.0
    for l in lots:
        if l.get("item_id") != item_id:
            continue
        if l.get("status") != "Released":
            continue
        if not _is_expiry_known(l):
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