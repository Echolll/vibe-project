def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "testauth",
        "email": "testauth@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testauth"
    assert data["email"] == "testauth@example.com"
    assert "id" in data


def test_register_validation_error(client):
    response = client.post("/auth/register", json={
        "username": "testauth2",
        "password": "password123"
    })
    assert response.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json={
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "password123"
    })

    response = client.post("/auth/login", data={
        "username": "logintest",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "wrongpwd",
        "email": "wrongpwd@example.com",
        "password": "password123"
    })

    response = client.post("/auth/login", data={
        "username": "wrongpwd",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный пароль"


def test_login_not_found(client):
    response = client.post("/auth/login", data={
        "username": "nonexistent",
        "password": "password123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Пользователь с таким логином не найден"
