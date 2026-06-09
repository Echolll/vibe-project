from datetime import datetime, timedelta
from backend.app.database.event import Events


def test_get_events_empty(client):
    response = client.get("/events/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_event_success(client, user_token_headers):
    future_date = (datetime.now() + timedelta(days=30)).isoformat()
    
    response = client.post("/events/", headers=user_token_headers, json={
        "title": "Поход в горы",
        "description": "Идём на Эльбрус",
        "date": future_date,
        "location": "Приэльбрусье",
        "max_participants": 10,
        "creator_id": 1
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Поход в горы"
    assert data["location"] == "Приэльбрусье"
    assert data["status"] == "active"
    assert "id" in data


def test_get_events_with_data(client, db):
    # Создаём событие напрямую в БД
    event = Events(
        title="Настолки",
        description="Играем в Мафию",
        date=datetime.now() + timedelta(days=7),
        location="Антикафе",
        max_participants=8,
        creator_id=1,
        status="active"
    )
    db.add(event)
    db.commit()
    
    response = client.get("/events/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Настолки"
    assert "date" in data[0]
    assert "status" in data[0]


def test_get_event_success(client, db):
    event = Events(
        title="Кино",
        description="Новый фильм",
        date=datetime.now() + timedelta(days=14),
        location="Кинотеатр",
        max_participants=15,
        creator_id=1,
        status="active"
    )
    db.add(event)
    db.commit()
    event_id = event.id
    
    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Кино"
    assert data["location"] == "Кинотеатр"
    assert data["description"] == "Новый фильм"
    assert data["status"] == "active"


def test_get_event_not_found(client):
    response = client.get("/events/99999")
    assert response.status_code == 404
    assert "не найдено" in response.json()["detail"].lower()


def test_create_event_missing_fields(client, user_token_headers):
    response = client.post("/events/", headers=user_token_headers, json={"title": "Только название"})
    assert response.status_code == 422


def test_create_event_invalid_date(client, user_token_headers):
    response = client.post("/events/", headers=user_token_headers, json={
        "title": "Событие",
        "date": "not-a-date",
        "location": "Место",
        "max_participants": 10,
        "creator_id": 1
    })
    assert response.status_code == 422


def test_update_event_success(client, db, user_token_headers):
    event = Events(
        title="Старое название",
        description="Старое описание",
        date=datetime.now() + timedelta(days=30),
        location="Старое место",
        max_participants=5,
        creator_id=1,
        status="active"
    )
    db.add(event)
    db.commit()
    event_id = event.id
    
    response = client.patch(f"/events/{event_id}", headers=user_token_headers, json={"title": "Новое название"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новое название"
    assert data["description"] == "Старое описание"


def test_update_event_partial(client, db, user_token_headers):
    event = Events(
        title="Для обновления",
        description="Описание",
        date=datetime.now() + timedelta(days=30),
        location="Место",
        max_participants=20,
        creator_id=1,
        status="active"
    )
    db.add(event)
    db.commit()
    event_id = event.id
    
    response = client.patch(f"/events/{event_id}", headers=user_token_headers, json={"max_participants": 50})
    assert response.status_code == 200
    assert response.json()["max_participants"] == 50


def test_update_event_not_found(client, user_token_headers):
    response = client.patch("/events/99999", headers=user_token_headers, json={"title": "Новое"})
    assert response.status_code == 404
    assert "не найдено" in response.json()["detail"].lower()


def test_delete_event_success(client, db, user_token_headers):
    event = Events(
        title="Для удаления",
        date=datetime.now() + timedelta(days=30),
        location="Место",
        max_participants=3,
        creator_id=1,
        status="active"
    )
    db.add(event)
    db.commit()
    event_id = event.id
    
    response = client.delete(f"/events/{event_id}", headers=user_token_headers)
    assert response.status_code == 204
    
    get_response = client.get(f"/events/{event_id}")
    assert get_response.status_code == 404


def test_delete_event_not_found(client, user_token_headers):
    response = client.delete("/events/99999", headers=user_token_headers)
    assert response.status_code == 404
    assert "не найдено" in response.json()["detail"].lower()