import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db import get_db, Base

TEST_FILE_NAME = "test_database.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_FILE_NAME}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def lifespan():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as tst_client:
        yield tst_client


@pytest.fixture()
def biblion_payload():
    biblion = {
        "name": "test_book",
        "author": "test_author",
        "publisher": "test_publisher",
        "description": "test_description",
    }
    return biblion

@pytest.fixture()
def updated_biblion_payload():
    updated_biblion = {
        "name": "updated_book",
        "author": "updated_author",
        "publisher": "updated_publisher",
        "description": "updated_description",
    }
    return updated_biblion

@pytest.fixture()
def credentials_payload():
    credentials = {"username": "test_user", "password": "user_password"}
    return credentials