def test_assign_game_to_cube(client):
    # Assign Kingdomino to r1c1
    response = client.post("/placements", json={
        "game_id": 204583,
        "fixture_id": 1,
        "slot": "r1c1"
    })

    assert response.status_code == 200
    placement = response.json()
    assert placement["slot"] == "r1c1"

    # Verify fixture reflects placement
    grid = client.get("/fixtures/1/grid").json()
    assert grid["r1c1"]["name"] == "Kingdomino"
