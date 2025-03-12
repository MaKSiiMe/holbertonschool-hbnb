#Part2/tests/test_place.py
def test_create_place(test_client):
    response = test_client.post('/api/v1/places/', json={
        "title": "Beach House",
        "price": 200,
        "latitude": 34.05,
        "longitude": -118.24
    })
    assert response.status_code == 201
    assert response.json["price"] == 200

def test_create_place_invalid_latitude(test_client):
    response = test_client.post('/api/v1/places/', json={
        "title": "Invalid Place",
        "price": 100,
        "latitude": 91,
        "longitude": 0
    })
    assert response.status_code == 400
    assert "Latitude must be between -90 and 90" in response.json["error"]
