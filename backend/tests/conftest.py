import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.routes.routes import app
from backend.app.database.database import Base, get_db
from backend.app.database.event import Events
from backend.app.database.user import Users
from backend.app.utils.security import hash_password

temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
TEST_DATABASE_URL = f"sqlite:///{temp_db_file.name}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

#Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope='function')
def client():
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope='function')
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope='function')
def user_token_headers(client, db):
    user = Users(
        username="main_user",
        email="main@test.com",
        password_hash=hash_password("password123")
    )
    db.add(user)
    db.commit()
    
    response = client.post("/auth/login", data={"username": "main_user", "password": "password123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope='function')
def other_user_token_headers(client, db):
    user = Users(
        username="other_user",
        email="other@test.com",
        password_hash=hash_password("password123")
    )
    db.add(user)
    db.commit()
    
    response = client.post("/auth/login", data={"username": "other_user", "password": "password123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def pytest_sessionfinish(session, exitstatus):
    try:
        temp_db_file.close()
        os.unlink(temp_db_file.name)
    except:
        pass