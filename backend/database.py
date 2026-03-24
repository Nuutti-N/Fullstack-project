from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv("database_url")
if not database_url:
    raise ValueError("Check your .env file")
engine = create_engine(database_url, echo=True)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
