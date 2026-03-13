from jose import jwt
from typing import Union, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os


Algorithm = "HS256"

context = CryptContext(schemes=["brycpt"], deprecated="auto")


def hash_password(password: str):
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return context.verify(plain_password, hashed_password)
