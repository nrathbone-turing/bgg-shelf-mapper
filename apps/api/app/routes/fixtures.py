from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Fixture, Placement, Game
from ..schemas import FixtureCreate, FixtureOut, FixtureGridOut, GridCell, GameOut

router = APIRouter(tags=["fixtures"])

_SLOT_RE = re.compile(r"^r(\d+)c(\d+)$")


def _parse_slot(slot: str) -> tuple[int, int]:
    m = _SLOT_RE.match(slot)
    if not m:
        raise ValueError("slot must look like r0c0")
    return int(m.group(1)), int(m.group(2))


@router.get("/api/fixtures", response_model=list[FixtureOut])
def list_fixtures(db: Session = Depends(get_db)) -> list[FixtureOut]:
    return [FixtureOut.model_validate(f) for f in db.query(Fixture).order_by(Fixture.id.asc()).all()]


@router.post("/api/fixtures", response_model=FixtureOut)
def create_fixture(payload: FixtureCreate, db: Session = Depends(get_db)) -> FixtureOut:
    fixture = Fixture(name=payload.name, rows=payload.rows, cols=payload.cols)
    db.add(fixture)
    db.commit()
    db.refresh(fixture)
    return FixtureOut.model_validate(fixture)


@router.get("/api/fixtures/{fixture_id}/grid", response_model=FixtureGridOut)
def get_fixture_grid(fixture_id: int, db: Session = Depends(get_db)) -> FixtureGridOut:
    fixture = db.get(Fixture, fixture_id)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    placements = db.query(Placement).filter(Placement.fixture_id == fixture.id).all()
    game_ids = [p.game_id for p in placements]
    games = db.query(Game).filter(Game.id.in_(game_ids)).all() if game_ids else []
    game_by_id = {g.id: g for g in games}
    placement_by_slot = {p.slot: p for p in placements}

    cells: list[GridCell] = []
    for r in range(fixture.rows):
        for c in range(fixture.cols):
            slot = f"r{r}c{c}"
            p = placement_by_slot.get(slot)
            if p:
                g = game_by_id.get(p.game_id)
                cells.append(
                    GridCell(
                        slot=slot,
                        game=GameOut.model_validate(g) if g else None,
                    )
                )
            else:
                cells.append(GridCell(slot=slot, game=None))

    return FixtureGridOut(
        fixture=FixtureOut.model_validate(fixture),
        cells=cells,
    )
