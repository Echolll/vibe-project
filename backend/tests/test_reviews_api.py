from backend.app.database.user import Users
from backend.app.database.event import Events
from backend.app.utils.security import hash_password
from datetime import datetime, timedelta

def test_create_review_success(client, db, user_token_headers):
    target_user = Users(
        username="target_user",
        email="target@test.com",
        password_hash=hash_password("password123")
    )
    db.add(target_user)
    db.commit()
    target_id = target_user.id

    event = Events(
        title="Событие для отзыва",
        date=datetime.now() + timedelta(days=5),
        location="Город",
        max_participants=10,
        creator_id=target_id,
        status="active"
    )
    db.add(event)
    db.commit()
    event_id = event.id

    response = client.post("/reviews/", headers=user_token_headers, json={
        "to_user_id": target_id,
        "event_id": event_id,
        "rating": 5,
        "comment": "Отличный организатор!"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Отличный организатор!"
    assert data["to_user_id"] == target_id

def test_create_review_self_forbidden(client, user_token_headers):
    me_resp = client.get("/users/me", headers=user_token_headers)
    my_id = me_resp.json()["id"]

    response = client.post("/reviews/", headers=user_token_headers, json={
        "to_user_id": my_id,
        "event_id": 1,
        "rating": 5,
        "comment": "Сам себя не похвалишь..."
    })
    
    assert response.status_code == 400
    assert "не можете поставить оценку самому себе" in response.json()["detail"].lower()

def test_get_user_reviews(client, db, user_token_headers):
    target_user = Users(
        username="target_user2",
        email="target2@test.com",
        password_hash=hash_password("password123")
    )
    db.add(target_user)
    db.commit()
    target_id = target_user.id

    client.post("/reviews/", headers=user_token_headers, json={
        "to_user_id": target_id,
        "event_id": 1,
        "rating": 4,
        "comment": "Хорошо"
    })
    client.post("/reviews/", headers=user_token_headers, json={
        "to_user_id": target_id,
        "event_id": 1,
        "rating": 5,
        "comment": "Отлично"
    })

    response = client.get(f"/reviews/user/{target_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    rating_response = client.get(f"/reviews/user/{target_id}/rating")
    assert rating_response.status_code == 200
    rating_data = rating_response.json()
    assert rating_data["average_rating"] == 4.5
    assert rating_data["reviews_count"] == 2
