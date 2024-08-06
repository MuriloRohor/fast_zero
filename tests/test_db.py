from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="marcelo",
        email="marcelo@email.com",
        password="minha_senha",
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == "marcelo@email.com")
    )

    assert result.username == "marcelo"
