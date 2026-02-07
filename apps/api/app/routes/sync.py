#apps/api/app/routes/sync.py
"""
BGG sync HTTP endpoint

This route:
- validates configuration
- delegates fetching to the BGG client
- delegates persistence to the sync service

It intentionally does NOT:
- parse XML
- contain DB upsert logic
- know anything about BGG API quirks
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.bgg.client import fetch_collection
from app.services.bgg_sync import upsert_games_from_bgg
from ..db import get_db
from ..schemas import SyncRequest

router = APIRouter(tags=["sync"])

@router.post("/api/sync/bgg")
def sync_bgg(payload: SyncRequest, db: Session = Depends(get_db)) -> dict:
    """
    Sync the user's owned BGG collection into the local database

    Current behavior:
    - Requires a BGG application token
    - Uses mocked BGG client in tests
    - Returns count of processed games

    Future behavior:
    - Retry on 202 (queued)
    - Throttle requests
    - Enrich with thing/details data
    """
    # Token can be supplied per-request or via environment
    token = payload.token or os.getenv("BGG_APP_TOKEN")
    if not token:
        raise HTTPException(
            # 501 is intentional: feature exists but is not configured
            status_code=501,
            detail="BGG sync is not configured yet.",
        )

    # Fetch external data (mocked in tests)
    try:
        items = fetch_collection(username=payload.username, token=token)
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="BGG sync is not wired up yet.",
        )

    # Persist data locally without touching placements
    processed = upsert_games_from_bgg(db=db, items=list(items))
    return {"status": "ok", "processed": processed}
