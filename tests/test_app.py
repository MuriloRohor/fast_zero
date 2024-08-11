from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")  # Act (alção)

    assert response.status_code == HTTPStatus.OK  # assert (afirmar)
    assert response.json() == {"message": "Olá mundo"}
