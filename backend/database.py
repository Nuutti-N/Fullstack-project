from sqlmodel import create_engine, Session
from backend.config import settings


# Don't check here .env url! Config already checked it! Use settings method! You don't need manual checking.
engine = create_engine(settings.database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
