from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
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


class TokenPayLoad(SQLModel):
    sub: str = None  # Username or Id
    exp: int = None  # Expiration


class SystemUser(SQLModel):
    id: int
    username: str
