from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="pedro",
        email="pedro@email.com",
        password="minha_senha",
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == "pedro@email.com")
    )

    assert result.username == "pedro"
