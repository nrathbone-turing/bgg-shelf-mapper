def test_list_fixtures(client):
    response = client.get("/fixtures")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Office Cubes (2x5)"
    assert data[0]["layout"]["rows"] == 2
    assert data[0]["layout"]["cols"] == 5
