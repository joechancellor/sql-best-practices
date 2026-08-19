from app.main import app


def test_advanced_search_returns_filtered_products():
    client = app.test_client()

    response = client.get(
        "/api/advanced-search",
        query_string={"category": "Electronics", "brand": "SoundMax", "in_stock": "1"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, list)
    assert payload
    assert all(item["category"] == "Electronics" for item in payload)
    assert all(item["brand"] == "SoundMax" for item in payload)
    assert all(item["is_in_stock"] == 1 for item in payload)
