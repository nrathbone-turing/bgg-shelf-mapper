from __future__ import annotations

"""
BGG integration placeholder.

BGG provides the "XML API2" endpoints (collection, thing, etc.). In mid/late 2025,
BGG began requiring registered "Application Tokens" sent as an Authorization: Bearer <token> header.

For now we keep this module as a stub so the app can ship with sample data first.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class BggCollectionItem:
    bgg_id: int
    name: str
    year_published: int | None
    thumbnail_url: str | None
    image_url: str | None


def fetch_collection(*, username: str, token: str) -> list[BggCollectionItem]:
    """
    TODO:
      - Call /xmlapi2/collection?username=...&own=1
      - Handle HTTP 202 "queued" responses by retrying with backoff
      - Throttle requests and cache responses
      - Optionally enrich with /xmlapi2/thing?id=... (max 20 IDs per request)
    """
    raise NotImplementedError("BGG sync is not wired up yet (seed/sample data only).")


def fetch_thing_details(*, ids: Iterable[int], token: str) -> dict[int, BggCollectionItem]:
    """Placeholder for future enrichment step."""
    raise NotImplementedError
