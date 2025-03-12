#Part2/tests/test_amenity.py
def test_create_amenity(test_client):
    response = test_client.post('/api/v1/amenities/', json={
        "name": "WiFi"
    })
    assert response.status_code == 201
    assert response.json["name"] == "WiFi"

def test_create_amenity_invalid(test_client):
    response = test_client.post('/api/v1/amenities/', json={
        "name": ""
    })
    assert response.status_code == 400
    assert "Amenity name cannot be empty" in response.json["error"]

