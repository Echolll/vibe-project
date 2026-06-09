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
from backend.app.utils.security import get_current_user

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

def override_get_current_user():
    return Users(id=1, username="test_user", email="test@test.com")

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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

def pytest_sessionfinish(session, exitstatus):
    try:
        temp_db_file.close()
        os.unlink(temp_db_file.name)
    except:
        pass