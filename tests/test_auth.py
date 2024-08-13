from http import HTTPStatus


def test_login_for_access_token(client, user):
    response = client.post(
        "/auth/token/",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_login_for_access_token_email_incorrect(client, user):
    response = client.post(
        "/auth/token/",
        data={
            "username": "email_errado@teste.com",
            "password": user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_for_access_token_password_incorrect(client, user):
    response = client.post(
        "/auth/token/",
        data={
            "username": user.email,
            "password": "senha_errada"
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}
