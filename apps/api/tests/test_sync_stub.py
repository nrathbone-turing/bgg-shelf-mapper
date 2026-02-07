#apps/api/tests/test_sync_stub.py
"""
BGG sync tests

These tests are intentionally layered:
1. Configuration validation (501 when missing token)
2. Client wiring validation (501 when client not implemented)
3. Contract test for successful sync (mocked BGG client)
"""

from app.bgg.client import BggCollectionItem


def test_bgg_sync_returns_501_without_token(client):
    response = client.post(
        "/api/sync/bgg",
        json={"username": "Piman34"},
    )

    assert response.status_code == 501
    assert "not configured" in response.json()["detail"].lower()


def test_bgg_sync_returns_501_when_client_not_implemented(client, mocker):
    mocker.patch(
        "app.routes.sync.fetch_collection",
        side_effect=NotImplementedError,
    )

    response = client.post(
        "/api/sync/bgg",
        json={"username": "Piman34", "token": "fake-token"},
    )

    assert response.status_code == 501
    assert "not wired up yet" in response.json()["detail"].lower()


def test_bgg_sync_creates_games_from_collection(client, mocker):
    """
    Contract test:
    - Given a mocked BGG collection
    - When sync is called
    - Then games exist in the local DB
    """
    mocker.patch(
        "app.routes.sync.fetch_collection",
        return_value=[
            BggCollectionItem(
                bgg_id=68448,
                name="7 Wonders",
                year_published=2010,
                thumbnail_url=None,
                image_url=None,
            )
        ],
    )

    response = client.post(
        "/api/sync/bgg",
        json={"username": "Piman34", "token": "fake-token"},
    )

    assert response.status_code == 200

    games = client.get("/api/games").json()
    assert any(game["name"] == "7 Wonders" for game in games)
