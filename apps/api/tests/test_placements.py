#apps/api/tests/test_placements.py
"""
Placement API tests

These tests verify:
- Slot assignment succeeds
- The API uses *local DB IDs* (not BGG IDs) when placing a game
- Fixture grid reflects placement changes

Important note:
- PlacementUpsert.game_id should be the local Game.id (primary key), NOT the BGG game id (bgg_id)
- Therefore the test fetches /api/games first and finds the right Game.id
"""


def _find_fixture_id(client, *, name: str) -> int:
    """Helper: find a fixture ID by name using the API."""
    resp = client.get("/api/fixtures")
    assert resp.status_code == 200, resp.text

    fixtures = resp.json()
    assert fixtures, "Expected at least one fixture to exist in seed data."

    for f in fixtures:
        if f.get("name") == name:
            return f["id"]

    # Fallback: pick first fixture if the expected name changes later
    return fixtures[0]["id"]


def _find_game_id_by_bgg_id(client, *, bgg_id: int) -> int:
    """Helper: find a local Game.id by BGG id using the API."""
    resp = client.get("/api/games")
    assert resp.status_code == 200, resp.text

    games = resp.json()
    assert games, "Expected at least one game to exist in seed data."

    for g in games:
        if g.get("bgg_id") == bgg_id:
            return g["id"]

    raise AssertionError(f"Expected to find a game with bgg_id={bgg_id} in seed data.")


def test_assign_game_to_cube(client):
    # Fixture: the seeded office cube grid
    fixture_id = _find_fixture_id(client, name="Office Cubes (2x5)")

    # Game: Kingdomino (BGG id 204583) -> convert to local DB id
    kingdomino_id = _find_game_id_by_bgg_id(client, bgg_id=204583)

    # Assign Kingdomino to bottom row, second column (r1c1)
    response = client.put(
        "/api/placements",
        json={
            "game_id": kingdomino_id,  # local DB id, not BGG id
            "fixture_id": fixture_id,
            "slot": "r1c1",
        },
    )

    assert response.status_code == 200, response.text
    placement = response.json()
    assert placement["slot"] == "r1c1"
    assert placement["fixture_id"] == fixture_id
    assert placement["game_id"] == kingdomino_id

    # Verify grid view reflects the new placement
    grid = client.get(f"/api/fixtures/{fixture_id}/grid").json()
    cells = {cell["slot"]: cell for cell in grid["cells"]}

    assert cells["r1c1"]["game"] is not None
    assert cells["r1c1"]["game"]["name"] == "Kingdomino"
    assert cells["r1c1"]["game"]["bgg_id"] == 204583
