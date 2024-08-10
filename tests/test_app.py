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


def test_create_user_where_username_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "Teste",
            "password": "teste",
            "email": "test_outro@test.com",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username alredy exists"}


def test_create_user_where_email_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "Teste_outro",
            "password": "teste",
            "email": "teste@test.com",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email alredy exists"}


def test_read_users(client):
    response = client.get(
        "/users/",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_user(client, user):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "Teste",
        "email": "teste@test.com",
    }


def test_read_user_not_found(client, user):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": user.clean_password,
            "id": user.id,
            "username": "testusername2",
            "email": "test@test.com",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": "testusername2",
        "email": "test@test.com",
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_get_token(client, user):
    response = client.post(
        "/token/",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
