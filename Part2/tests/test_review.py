#Part2/tests/test_review.py
def test_create_review(test_client):
    # Create dependencies (user and place)
    user_response = test_client.post('/api/v1/users/', json={
        "first_name": "User",
        "last_name": "One",
        "email": "user@example.com"
    })
    place_response = test_client.post('/api/v1/places/', json={
        "title": "Test Place",
        "price": 150,
        "latitude": 0,
        "longitude": 0
    })
    
    response = test_client.post('/api/v1/reviews/', json={
        "text": "Great place!",
        "user_id": user_response.json["id"],
        "place_id": place_response.json["id"]
    })
    assert response.status_code == 201
    assert response.json["text"] == "Great place!"

def test_create_review_invalid_user(test_client):
    response = test_client.post('/api/v1/reviews/', json={
        "text": "Invalid user",
        "user_id": "invalid-id",
        "place_id": "valid-id"
    })
    assert response.status_code == 400
    assert "Invalid user_id" in response.json["error"]
