from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "teste",
            "password": "teste",
            "email": "teste@teste.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    # Validar UserPublic
    assert response.json() == {
        "id": 2,
        "username": "teste",
        "email": "teste@teste.com",
    }


def test_create_user_where_username_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "password": "teste",
            "email": "teste_diferente@email.com",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username alredy exists"}


def test_create_user_where_email_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "teste",
            "password": "teste",
            "email": user.email,
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
    response = client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": user.username,
        "email": user.email,
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


def test_update_wrong_user(client, user, token):
    response = client.put(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": user.clean_password,
            "id": user.id,
            "username": "testusername2",
            "email": "test@test.com",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}
