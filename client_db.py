from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_user_id: Optional[str] = None
    yandex_user_id: Optional[str] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_user(telegram_user_id: str | None = None, yandex_user_id: str | None = None) -> User:
    user = User(telegram_user_id=telegram_user_id, yandex_user_id=yandex_user_id)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        return user


def get_user(yandex_user_id=None, telegram_user_id=None):
    assert yandex_user_id or telegram_user_id, 'Нужен хотя бы один id'

    query = select(User)
    if yandex_user_id:
        query = query.where(User.yandex_user_id == yandex_user_id)
    if telegram_user_id:
        query = query.where(User.telegram_user_id == telegram_user_id)

    with Session(engine) as session:
        results = session.exec(query)
        return results.one_or_none()
