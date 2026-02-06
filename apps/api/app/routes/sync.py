from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import SyncRequest
from ..bgg.client import fetch_collection

router = APIRouter(tags=["sync"])


@router.post("/api/sync/bgg")
def sync_bgg(payload: SyncRequest, db: Session = Depends(get_db)) -> dict:
    """
    Sync the user's BGG collection into the local database.
    """
    token = payload.token or os.getenv("BGG_APP_TOKEN")
    if not token:
        raise HTTPException(
            status_code=501,
            detail=(
                "BGG sync is not configured yet. "
                "Later you'll set BGG_APP_TOKEN (Authorization: Bearer <token>) and enable real syncing."
            ),
        )

    try:
        # Will raise NotImplementedError for now
        fetch_collection(username=payload.username, token=token)
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="BGG sync is not wired up yet (seed/sample data only).",
        )

    # Will only be reachable once implemented
    return {"status": "ok"}
