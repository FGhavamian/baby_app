from fastapi import status
from jose import jwt
import pytest

from app import schemas

from app.config import settings


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, settings.algorithm
    )
    id: str = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong_email", "123", status.HTTP_403_FORBIDDEN),
        ("f@g.com", "wrong_password", status.HTTP_403_FORBIDDEN),
        ("wrong_email", "wrong_password", status.HTTP_403_FORBIDDEN),
        (None, "123", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("f@g.com", None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code


def test_create_user(client):
    res = client.post("/users", json={"email": "f@g.com", "password": "123"})

    new_user = schemas.User(**res.json())
    assert new_user.email == "f@g.com"
    assert res.status_code == status.HTTP_201_CREATED
