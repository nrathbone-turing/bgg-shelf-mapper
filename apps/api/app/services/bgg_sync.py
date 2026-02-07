#apps/api/app/services/bgg_sync.py
"""
BGG sync domain logic

This module is intentionally minimal:
- No FastAPI imports
- No HTTP concerns
- No request/response schemas

Its only job is to translate BGG collection items into local database state
"""

from sqlalchemy.orm import Session

from app.bgg.client import BggCollectionItem
from app.models import Game


def upsert_games_from_bgg(db: Session, items: list[BggCollectionItem]) -> int:
    """
    Insert or update games based on BGG collection data

    Rules:
    - `bgg_id` is the natural unique key
    - Existing games are updated in-place
    - New games are inserted
    - No placements are touched (location data is local-only)

    Returns:
        int: number of games processed
    """
    processed = 0

    for item in items:
        # Look up by BGG ID (stable external identifier)
        game = db.query(Game).filter(Game.bgg_id == item.bgg_id).one_or_none()

        if game is None:
            # New game discovered via BGG
            game = Game(
                bgg_id=item.bgg_id,
                name=item.name,
                year_published=item.year_published,
                thumbnail_url=item.thumbnail_url,
                image_url=item.image_url,
            )
            db.add(game)
        else:
            # Existing game: update metadata only
            game.name = item.name
            game.year_published = item.year_published
            game.thumbnail_url = item.thumbnail_url
            game.image_url = item.image_url

        processed += 1

    # One commit at the end keeps behavior predictable
    db.commit()
    return processed
