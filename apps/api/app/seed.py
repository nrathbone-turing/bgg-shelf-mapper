from __future__ import annotations

from sqlalchemy.orm import Session

from .models import Game, Fixture, Placement


SAMPLE_GAMES = [
    # From the links you shared:
    {"bgg_id": 68448, "name": "7 Wonders", "year_published": 2010},
    {"bgg_id": 199042, "name": "Harry Potter: Hogwarts Battle", "year_published": 2016},
    {"bgg_id": 206931, "name": "Encore!", "year_published": 2016},
    {"bgg_id": 40692, "name": "Small World", "year_published": 2009},
    {"bgg_id": 92415, "name": "Skull", "year_published": 2011},
    {"bgg_id": 204583, "name": "Kingdomino", "year_published": 2016},
]


def seed_if_empty(db: Session) -> None:
    # Create fixture if none exist
    if db.query(Fixture).count() == 0:
        fixture = Fixture(name="Office Cubes (2x5)", rows=2, cols=5)
        db.add(fixture)
        db.commit()
    else:
        fixture = db.query(Fixture).order_by(Fixture.id.asc()).first()

    # Add sample games if none exist
    if db.query(Game).count() == 0:
        for g in SAMPLE_GAMES:
            db.add(Game(**g, thumbnail_url=None, image_url=None))
        db.commit()

    # Add a couple sample placements if empty
    if db.query(Placement).count() == 0:
        games = db.query(Game).order_by(Game.id.asc()).all()
        # Place first 5 across top row
        for i, game in enumerate(games[:5]):
            db.add(Placement(fixture_id=fixture.id, slot=f"r0c{i}", game_id=game.id))
        # Place 6th in bottom-left if present
        if len(games) > 5:
            db.add(Placement(fixture_id=fixture.id, slot="r1c0", game_id=games[5].id))
        db.commit()
