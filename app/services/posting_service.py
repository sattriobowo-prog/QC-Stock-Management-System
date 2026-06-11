"""Phase 2 service-layer posting plan builders.

These helpers compose the immutable payloads required to post a
stock-changing event: a lot row (when applicable), a StockBalance upsert
plan, a StockTransaction ledger row, and an AuditLog entry. They are
*pure* — they never mutate state and never touch the database — so they
can be used safely from event handlers, background tasks, and tests
before the persistent tables exist.

GxP / CSV evidence collection points:
  * Every payload returned here is shaped 1:1 with the persistent
    foundation schemas in app.models.schemas. A future ORM layer can
    persist these dicts verbatim inside `async with rx.asession() as s:`
    using SQLAlchemy `text()` raw SQL inserts (per Reflex-hosted DB
    pattern). The append-only StockTransaction + AuditLog combo is the
    GxP audit trail of record.
  * Opening-balance posting (`build_opening_balance_post`) is the entry
    point for migration commit. The lot/balance/transaction/audit quad
    is grouped so the caller can wrap a single transaction around them
    when persistence lands.
"""

from __future__ import annotations
from datetime import datetime
import uuid
import logging

from app.services.permissions import require_permission
from app.services.stock_service import (
    validate_stock_change,
    eligible_lots_for_issue,
    fefo_allocation,
    validate_fefo_override,
)
from app.services.audit_service import (
    build_audit_entry,
    build_transaction_entry,
)
from app.services.migration_service import (
    build_opening_balance_lot,
    build_opening_balance_transaction,
    normalize_location,
    normalize_migration_lot,
    MIGRATION_LOCATION,
    MIGRATION_TRANSACTION_TYPE,
)


# ---------------------------------------------------------------------------
# Stock balance upsert planning
# ---------------------------------------------------------------------------


def build_stock_balance_upsert_plan(
    item_id: str,
    lot_number: str,
    location: str,
    delta: float,
    unit: str,
) -> dict:
    """Pure plan describing a StockBalance upsert by (item, lot, location).

    The returned plan does not mutate state — the caller (or a future
    `async with rx.asession()` block) is responsible for SELECT-then-
    INSERT-or-UPDATE using the unique key. Negative-stock projection is
    NOT validated here; validate via `validate_stock_change` first.
    """
    return {
        "operation": "upsert_stock_balance",
        "key": {
            "item_id": item_id,
            "lot_number": lot_number,
            "location": normalize_location(location),
        },
        "delta": float(delta),
        "unit": unit,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ---------------------------------------------------------------------------
# Generic stock-movement post (issue / receive / adjust / transfer leg)
# ---------------------------------------------------------------------------


def build_stock_movement_post(
    *,
    transaction_type: str,
    item_id: str,
    lot_number: str,
    location: str,
    delta: float,
    unit: str,
    user: str,
    role: str,
    required_permission: str = "",
    on_hand: float | None = None,
    reference: str = "",
    notes: str = "",
    audit_action: str = "",
    audit_detail: str = "",
) -> tuple[bool, str, dict]:
    """Compose the four-payload bundle for a single stock-movement post.

    Returns (ok, reason, plan). On failure `plan` is empty. On success
    plan = {balance_plan, transaction, audit}. Caller persists in one
    transaction (lot upsert if needed is the caller's responsibility).
    """
    if required_permission:
        ok, reason = require_permission(role, required_permission)
        if not ok:
            return (False, reason, {})

    if on_hand is not None:
        ok, reason, _ = validate_stock_change(on_hand, delta, unit)
        if not ok:
            return (False, reason, {})

    balance_plan = build_stock_balance_upsert_plan(
        item_id=item_id,
        lot_number=lot_number,
        location=location,
        delta=delta,
        unit=unit,
    )
    transaction = build_transaction_entry(
        transaction_type=transaction_type,
        item_id=item_id,
        lot_number=lot_number,
        delta=delta,
        unit=unit,
        user=user,
        role=role,
        reference=reference,
        notes=notes,
    )
    audit = build_audit_entry(
        user=user,
        role=role,
        action=audit_action or transaction_type.upper(),
        target=f"{item_id} / {lot_number}",
        detail=audit_detail
        or f"Δ{delta} {unit} @ {normalize_location(location)} ({transaction_type})",
    )
    return (
        True,
        "OK",
        {
            "balance_plan": balance_plan,
            "transaction": transaction,
            "audit": audit,
        },
    )


# ---------------------------------------------------------------------------
# FEFO issue post (multi-lot allocation)
# ---------------------------------------------------------------------------


def build_fefo_issue_post(
    *,
    lots: list[dict],
    item_id: str,
    quantity: float,
    unit: str,
    user: str,
    role: str,
    chosen_lot_number: str = "",
    override_reason: str = "",
    override_comment: str = "",
    recipient: str = "",
    purpose: str = "",
) -> tuple[bool, str, dict]:
    """Plan a FEFO issue post.

    * Permission `issue_stock` is required.
    * If `chosen_lot_number` is empty, FEFO multi-lot allocation is used.
    * If `chosen_lot_number` is provided AND it differs from the FEFO
      lot, both `override_reason` and `override_comment` are required
      (validated via `validate_fefo_override`).

    Returns (ok, reason, plan) with plan = {allocations, transactions,
    audits, balance_plans}. Caller persists in one DB transaction.
    """
    ok, reason = require_permission(role, "issue_stock")
    if not ok:
        return (False, reason, {})

    eligible = eligible_lots_for_issue(lots, item_id)
    if not eligible:
        return (
            False,
            "No Released, non-expired lots are available for this item.",
            {},
        )
    fefo_lot = eligible[0]

    if chosen_lot_number and chosen_lot_number != fefo_lot.get("lot_number"):
        chosen = next(
            (l for l in eligible if l.get("lot_number") == chosen_lot_number),
            None,
        )
        if chosen is None:
            return (
                False,
                f"Lot {chosen_lot_number} is not eligible for issue (must be Released, non-expired).",
                {},
            )
        ok, reason = validate_fefo_override(
            chosen, fefo_lot, override_reason, override_comment
        )
        if not ok:
            return (False, reason, {})
        if not override_comment.strip():
            return (
                False,
                "FEFO override comment is required for GxP audit defensibility.",
                {},
            )
        allocations = [(chosen, float(quantity))]
        if float(chosen.get("quantity", 0)) < quantity:
            return (
                False,
                f"Lot {chosen_lot_number} only has {chosen.get('quantity', 0)} {unit}.",
                {},
            )
    else:
        ok, reason, allocations = fefo_allocation(lots, item_id, quantity)
        if not ok:
            return (False, reason, {})

    balance_plans: list[dict] = []
    transactions: list[dict] = []
    audits: list[dict] = []
    for lot, draw in allocations:
        balance_plans.append(
            build_stock_balance_upsert_plan(
                item_id=item_id,
                lot_number=lot.get("lot_number", ""),
                location=lot.get("location", ""),
                delta=-float(draw),
                unit=unit,
            )
        )
        transactions.append(
            build_transaction_entry(
                transaction_type="issue",
                item_id=item_id,
                lot_number=lot.get("lot_number", ""),
                delta=-float(draw),
                unit=unit,
                user=user,
                role=role,
                reference=recipient,
                notes=purpose,
            )
        )
        detail = (
            f"Issued {draw} {unit} from {lot.get('lot_number', '')} "
            f"to {recipient or '-'} for {purpose or '-'}"
        )
        if override_reason and lot.get("lot_number") != fefo_lot.get(
            "lot_number"
        ):
            detail += (
                f" [FEFO OVERRIDE — reason: {override_reason}; "
                f"comment: {override_comment}]"
            )
        audits.append(
            build_audit_entry(
                user=user,
                role=role,
                action="ISSUE",
                target=f"{item_id} / {lot.get('lot_number', '')}",
                detail=detail,
            )
        )

    plan = {
        "fefo_lot": fefo_lot.get("lot_number", ""),
        "allocations": [
            {"lot_number": l.get("lot_number"), "quantity": q}
            for l, q in allocations
        ],
        "balance_plans": balance_plans,
        "transactions": transactions,
        "audits": audits,
        "override_used": bool(
            chosen_lot_number
            and chosen_lot_number != fefo_lot.get("lot_number")
        ),
    }
    return (True, "OK", plan)


# ---------------------------------------------------------------------------
# Opening balance posting foundation
# ---------------------------------------------------------------------------


def build_opening_balance_post(
    *,
    item_id: str,
    item_name: str,
    sku: str,
    quantity: float,
    unit: str,
    expiry: str | None,
    location: str | None,
    user: str,
    role: str,
    raw_lot: str = "",
    row_no: int = 0,
    batch_no: str = "",
) -> tuple[bool, str, dict]:
    """Compose the migration opening-balance four-payload bundle.

    Permission: `migration_commit` (Admin only). Returns
    (ok, reason, plan) with:
        plan["lot"]         — Lot row payload (MIG-<sku>,
                              expiry_known/expiry_date per spec,
                              qc_status='released',
                              location 'MIGRATION / UNASSIGNED',
                              transaction_type='opening_balance')
        plan["balance_plan"] — StockBalance upsert plan
        plan["transaction"]  — StockTransaction (transaction_type
                              exactly 'opening_balance')
        plan["audit"]        — AuditLog entry

    Caller persists all four inside a single DB transaction. Negative
    quantity is rejected with an explicit error (no silent clamp).
    """
    ok, reason = require_permission(role, "migration_commit")
    if not ok:
        return (False, reason, {})

    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        return (False, "Opening balance quantity is not numeric.", {})

    if qty < 0:
        return (
            False,
            "Negative opening balances are rejected without silent clamping.",
            {},
        )

    try:
        lot_payload = build_opening_balance_lot(
            item_id=item_id,
            item_name=item_name,
            sku=sku,
            quantity=qty,
            unit=unit,
            expiry=expiry,
            location=location,
            raw_lot=raw_lot,
            row_no=row_no,
        )
    except ValueError as e:
        logging.exception(f"Opening balance lot build failed: {e}")
        return (False, str(e), {})

    # Force qc_status to lower-case 'released' per Phase 2 contract.
    lot_payload["qc_status"] = "released"

    lot_number = lot_payload["lot_number"]
    loc = lot_payload["location"]

    balance_plan = build_stock_balance_upsert_plan(
        item_id=item_id,
        lot_number=lot_number,
        location=loc,
        delta=qty,
        unit=unit,
    )
    transaction = build_opening_balance_transaction(
        item_id=item_id,
        lot_number=lot_number,
        quantity=qty,
        unit=unit,
        location=loc,
        user=user,
        role=role,
        batch_no=batch_no,
    )
    audit = build_audit_entry(
        user=user,
        role=role,
        action="OPENING_BALANCE",
        target=f"{item_id} / {lot_number}",
        detail=(
            f"Migrated opening balance {qty} {unit} → {loc} "
            f"(Released, batch={batch_no or 'manual'})"
        ),
    )

    return (
        True,
        "OK",
        {
            "lot": lot_payload,
            "balance_plan": balance_plan,
            "transaction": transaction,
            "audit": audit,
        },
    )


__all__ = [
    "build_stock_balance_upsert_plan",
    "build_stock_movement_post",
    "build_fefo_issue_post",
    "build_opening_balance_post",
]