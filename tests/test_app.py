from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")  # Act (alção)

    assert response.status_code == HTTPStatus.OK  # assert (afirmar)
    assert response.json() == {"message": "Olá mundo"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testeusername",
            "password": "password",
            "email": "test@test.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    # Validar UserPublic
    assert response.json() == {
        "id": 1,
        "username": "testeusername",
        "email": "test@test.com",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "password": "123",
            "id": 1,
            "username": "testusername2",
            "email": "test@test.com",
        },
    )
    assert response.json() == {
        "id": 1,
        "username": "testusername2",
        "email": "test@test.com",
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.json() == {"message": "User deleted"}
