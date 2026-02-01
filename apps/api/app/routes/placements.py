from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Fixture, Game, Placement
from ..schemas import PlacementUpsert, PlacementOut

router = APIRouter(tags=["placements"])

_SLOT_RE = re.compile(r"^r(\d+)c(\d+)$")


def _parse_slot(slot: str) -> tuple[int, int]:
    m = _SLOT_RE.match(slot)
    if not m:
        raise ValueError("slot must look like r0c0")
    return int(m.group(1)), int(m.group(2))


@router.put("/api/placements", response_model=PlacementOut)
def upsert_placement(payload: PlacementUpsert, db: Session = Depends(get_db)) -> PlacementOut:
    fixture = db.get(Fixture, payload.fixture_id)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    game = db.get(Game, payload.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        r, c = _parse_slot(payload.slot)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if r < 0 or c < 0 or r >= fixture.rows or c >= fixture.cols:
        raise HTTPException(status_code=400, detail="slot is out of bounds for this fixture")

    # Remove any previous placement for this game (a game can only be in one slot)
    db.query(Placement).filter(Placement.game_id == game.id).delete(synchronize_session=False)
    # Remove any previous game in this slot
    db.query(Placement).filter(
        Placement.fixture_id == fixture.id,
        Placement.slot == payload.slot,
    ).delete(synchronize_session=False)

    placement = Placement(fixture_id=fixture.id, slot=payload.slot, game_id=game.id)
    db.add(placement)
    db.commit()
    db.refresh(placement)
    return PlacementOut.model_validate(placement)


@router.delete("/api/placements/{fixture_id}/{slot}")
def clear_slot(fixture_id: int, slot: str, db: Session = Depends(get_db)) -> dict:
    fixture = db.get(Fixture, fixture_id)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    deleted = db.query(Placement).filter(
        Placement.fixture_id == fixture.id,
        Placement.slot == slot,
    ).delete(synchronize_session=False)
    db.commit()
    return {"deleted": deleted}
