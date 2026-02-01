from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import SyncRequest

router = APIRouter(tags=["sync"])


@router.post("/api/sync/bgg")
def sync_bgg(payload: SyncRequest, db: Session = Depends(get_db)) -> dict:
    """
    Placeholder endpoint.

    When implemented, this will:
      - download your BGG owned collection
      - upsert games into the local DB
      - keep your fixture placements intact
    """
    token = payload.token or os.getenv("BGG_APP_TOKEN")
    if not token:
        # Using 501 ("Not Implemented") intentionally while this is a placeholder.
        raise HTTPException(
            status_code=501,
            detail=(
                "BGG sync is not configured yet. "
                "Later you'll set BGG_APP_TOKEN (Authorization: Bearer <token>) and enable real syncing."
            ),
        )

    raise HTTPException(status_code=501, detail="BGG sync is not wired up yet (seed/sample data only).")
