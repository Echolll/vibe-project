from backend.app.utils.security import hash_password
from backend.app.database.user import Users

def test_get_user_me(client, user_token_headers):
    response = client.get("/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "main_user"
    assert data["email"] == "main@test.com"

def test_get_user_by_id(client, db):
    user = Users(
        username="search_user",
        email="search@test.com",
        password_hash=hash_password("password123")
    )
    db.add(user)
    db.commit()
    user_id = user.id

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "search_user"

def test_get_user_not_found(client):
    response = client.get("/users/99999")
    assert response.status_code == 404

def test_update_user_me(client, user_token_headers, db):
    me_resp = client.get("/users/me", headers=user_token_headers)
    user_id = me_resp.json()["id"]

    response = client.patch(f"/users/{user_id}", headers=user_token_headers, json={"full_name": "Новое Имя"})
    assert response.status_code == 200
    assert response.json()["full_name"] == "Новое Имя"

def test_update_other_user_forbidden(client, other_user_token_headers, db):
    user = Users(
        username="target_user",
        email="target@test.com",
        password_hash=hash_password("password123")
    )
    db.add(user)
    db.commit()
    target_id = user.id

    response = client.patch(f"/users/{target_id}", headers=other_user_token_headers, json={"full_name": "Хакер"})
    assert response.status_code == 403

def test_update_password_me(client, user_token_headers):
    me_resp = client.get("/users/me", headers=user_token_headers)
    user_id = me_resp.json()["id"]

    response = client.patch(f"/users/{user_id}/password", headers=user_token_headers, json={"password": "new_password123"})
    assert response.status_code == 200

    login_resp = client.post("/auth/login", data={"username": "main_user", "password": "new_password123"})
    assert login_resp.status_code == 200

def test_delete_user_me(client, db):
    user = Users(
        username="delete_user",
        email="delete@test.com",
        password_hash=hash_password("delete123")
    )
    db.add(user)
    db.commit()
    user_id = user.id

    login_resp = client.post("/auth/login", data={"username": "delete_user", "password": "delete123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.request("DELETE", f"/users/{user_id}", headers=headers, json={"password": "delete123"})
    assert response.status_code == 204

    check_resp = client.get(f"/users/{user_id}")
    assert check_resp.status_code == 404
