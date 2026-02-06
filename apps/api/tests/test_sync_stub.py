def test_bgg_sync_returns_501_when_not_configured(client):
    response = client.post(
        "/api/sync/bgg",
        json={"token": None}
    )

    assert response.status_code == 501
    assert "not configured" in response.json()["detail"].lower()

def test_bgg_sync_with_token_still_not_implemented(client):
    response = client.post(
        "/api/sync/bgg",
        json={"token": "fake-token"}
    )

    assert response.status_code == 501
    assert "not wired up yet" in response.json()["detail"].lower()

def test_bgg_sync_creates_games_from_bgg_collection(client, mocker):
    mocker.patch(
        "app.bgg.client.fetch_collection",
        return_value=[
            {
                "bgg_id": 68448,
                "name": "7 Wonders",
                "year": 2010,
            }
        ],
    )

    response = client.post(
        "/api/sync/bgg",
        json={"token": "fake-token"}
    )

    assert response.status_code == 200

    games = client.get("/games").json()
    assert any(g["name"] == "7 Wonders" for g in games)
