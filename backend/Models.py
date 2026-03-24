from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    Email: str


class UserAuth(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


class token(BaseModel):
    access_token: str
    refresh_token: str
