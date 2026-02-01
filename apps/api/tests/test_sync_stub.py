def test_bgg_sync_stub(client, mocker):
    mocker.patch(
        "app.bgg.client.fetch_collection",
        return_value=[
            {
                "bgg_id": 68448,
                "name": "7 Wonders",
                "year": 2010
            }
        ]
    )

    response = client.post("/sync/bgg")
    assert response.status_code == 200

    games = client.get("/games").json()
    assert any(g["name"] == "7 Wonders" for g in games)
