from fastapi import status
import pytest

from app import schemas


@pytest.mark.parametrize(("baby_id"), [(1), (2), (3)])
def test_get_baby(authorized_client, test_babies, baby_id):
    res = authorized_client.get(f"/babies/{baby_id}")
    schemas.Baby(**res.json())
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(("baby_id"), [(1), (2), (3)])
def test_unauthorized_user_get_baby(client, test_babies, baby_id):
    res = client.get(f"/babies/{baby_id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
