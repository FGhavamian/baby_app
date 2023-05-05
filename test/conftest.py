from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pytest

from app.main import app
from app import database
from app.config import settings
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "f@g.com", "password": "123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == status.HTTP_201_CREATED

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_babies(test_user, session):
    babies_data = [
        {"name": "liam", "user_id": test_user["id"]},
        {"name": "rayan", "user_id": test_user["id"]},
        {"name": "sofi", "user_id": test_user["id"]},
    ]

    def create_baby_model(baby):
        return models.Babies(**baby)

    baby_map = map(create_baby_model, babies_data)
    babies = list(baby_map)

    # session.add_all([models.Babies(**baby_data) for baby_data in babies_data])
    session.add_all(babies)

    session.commit()

    babies = session.query(models.Babies).all()
    # print(babies)

    return babies
