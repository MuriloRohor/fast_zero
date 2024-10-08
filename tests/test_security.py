from http import HTTPStatus

import pytest
from fastapi.exceptions import HTTPException
from jwt import decode

from fast_zero.security import create_access_token, get_current_user, settings


def test_jwt():
    data = {"sub": "test@test.com"}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result["sub"] == data["sub"]
    assert result["exp"]


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_current_no_sub(user):
    token = create_access_token({"no_sub": "teste@teste.com"})

    with pytest.raises(HTTPException):
        get_current_user(user, token)


def test_get_current_user_not_found(session):
    token = create_access_token({"sub": "t2este@teste.com"})

    with pytest.raises(HTTPException):
        get_current_user(session, token)
