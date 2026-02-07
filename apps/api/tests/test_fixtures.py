#apps/api/tests/test_fixtures.py
def test_list_fixtures(client):
    response = client.get("/api/fixtures")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Office Cubes (2x5)"
    assert data[0]["rows"] == 2
    assert data[0]["cols"] == 5