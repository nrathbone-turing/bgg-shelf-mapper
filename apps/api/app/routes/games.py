from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Game, Placement
from ..schemas import GameWithPlacementOut

router = APIRouter(tags=["games"])


@router.get("/api/games", response_model=list[GameWithPlacementOut])
def list_games(
    q: str | None = Query(default=None, description="Case-insensitive name search"),
    db: Session = Depends(get_db),
) -> list[GameWithPlacementOut]:
    qry = db.query(Game, Placement).outerjoin(Placement, Placement.game_id == Game.id)
    if q:
        qry = qry.filter(Game.name.ilike(f"%{q}%"))
    rows = qry.order_by(Game.name.asc()).all()

    results: list[GameWithPlacementOut] = []
    for game, placement in rows:
        results.append(
            GameWithPlacementOut(
                id=game.id,
                bgg_id=game.bgg_id,
                name=game.name,
                year_published=game.year_published,
                thumbnail_url=game.thumbnail_url,
                image_url=game.image_url,
                fixture_id=placement.fixture_id if placement else None,
                slot=placement.slot if placement else None,
            )
        )
    return results
