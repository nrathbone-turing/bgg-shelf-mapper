#apps/api/app/schemas.py
from __future__ import annotations

from pydantic import BaseModel, Field


class GameOut(BaseModel):
    id: int
    bgg_id: int
    name: str
    year_published: int | None = None
    thumbnail_url: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True


class GameWithPlacementOut(GameOut):
    fixture_id: int | None = None
    slot: str | None = None


class FixtureCreate(BaseModel):
    name: str = Field(min_length=1)
    rows: int = Field(ge=1, le=50)
    cols: int = Field(ge=1, le=50)


class FixtureOut(BaseModel):
    id: int
    name: str
    rows: int
    cols: int

    class Config:
        from_attributes = True


class PlacementUpsert(BaseModel):
    fixture_id: int
    slot: str  # r{row}c{col}
    game_id: int


class PlacementOut(BaseModel):
    id: int
    fixture_id: int
    slot: str
    game_id: int

    class Config:
        from_attributes = True


class GridCell(BaseModel):
    slot: str
    game: GameOut | None = None


class FixtureGridOut(BaseModel):
    fixture: FixtureOut
    # mapping slot -> game (null if empty)
    cells: list[GridCell]


class SyncRequest(BaseModel):
    username: str
    # Not required for now; we keep it to make wiring easy later.
    token: str | None = None
