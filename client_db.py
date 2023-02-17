from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_user_id: str
    yandex_user_id: Optional[str] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_user(user, telegram_user_id):
    user = User(telegram_user_id=telegram_user_id)

    with Session(engine) as session:
        session.add(user)
        session.commit()


def get_user(yandex_user_id):
    with Session(engine) as session:
        statement = select(User).where(User.yandex_user_id == yandex_user_id)
        results = session.exec(statement)
        return results.one_or_none()
