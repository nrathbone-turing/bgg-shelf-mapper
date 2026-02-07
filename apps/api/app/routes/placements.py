#apps/api/app/routes/placements.py
"""
Placement (location) API

Owns physical location state:
- Which game is in which fixture slot
- Slot validation and bounds checking
- Enforces one-game-per-slot and one-slot-per-game

This data is intentionally local-only and never synced to BGG
"""

from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Fixture, Game, Placement
from ..schemas import PlacementUpsert, PlacementOut


router = APIRouter(
    prefix="/api",
    tags=["placements"],
)

_SLOT_RE = re.compile(r"^r(\d+)c(\d+)$")


def _parse_slot(slot: str) -> tuple[int, int]:
    """Parse a slot string into row/column integers"""
    match = _SLOT_RE.match(slot)
    if not match:
        raise ValueError("slot must look like r0c0")
    return int(match.group(1)), int(match.group(2))


@router.put("/placements", response_model=PlacementOut)
def upsert_placement(
    payload: PlacementUpsert,
    db: Session = Depends(get_db),
) -> PlacementOut:
    fixture = db.get(Fixture, payload.fixture_id)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    game = db.get(Game, payload.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        row, col = _parse_slot(payload.slot)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if row < 0 or col < 0 or row >= fixture.rows or col >= fixture.cols:
        raise HTTPException(
            status_code=400,
            detail="slot is out of bounds for this fixture",
        )

    # Enforce uniqueness
    db.query(Placement).filter(
        Placement.game_id == game.id
    ).delete(synchronize_session=False)

    db.query(Placement).filter(
        Placement.fixture_id == fixture.id,
        Placement.slot == payload.slot,
    ).delete(synchronize_session=False)

    placement = Placement(
        fixture_id=fixture.id,
        slot=payload.slot,
        game_id=game.id,
    )

    db.add(placement)
    db.commit()
    db.refresh(placement)

    return PlacementOut.model_validate(placement)


@router.delete("/placements/{fixture_id}/{slot}")
def clear_slot(
    fixture_id: int,
    slot: str,
    db: Session = Depends(get_db),
) -> dict:
    fixture = db.get(Fixture, fixture_id)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    deleted = db.query(Placement).filter(
        Placement.fixture_id == fixture.id,
        Placement.slot == slot,
    ).delete(synchronize_session=False)

    db.commit()
    return {"deleted": deleted}
