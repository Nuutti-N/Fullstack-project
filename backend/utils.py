from jose import jwt
from typing import Union, Any
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
load_dotenv()

access_token_expire_minutes = 30
refresh_token = 60 * 24 * 7
algorithm = "HS256"
jwt_key = os.environ["jwt_key"]
jwt_refresh_key = os.environ["jwt_refresh_key"]

# machine (cryptcontext) use a special way to scramble calle brycpt and if you find old ways update automatically
context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:  # When user registers
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:  # When user logs in
    return context.verify(plain_password, hashed_password)


# After succesful login, send this to frontend
def create_access_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        # UTC is little bit risk, because its work only 3.11 up versions. I recommend use timezone.utc, but risk to risk
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        # UTC is little bit risk, because its work only 3.11 up versions. I recommend use timezone.utc, but risk to risk
        expires_delta = datetime.now(
            UTC) + timedelta(minutes=access_token_expire_minutes)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, jwt_key, algorithm)
    return encoded_jwt

# After succesful login, send this too


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        # UTC is little bit risk, because its work only 3.11 up versions. I recommend use timezone.utc, but risk to risk
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        # UTC is little bit risk, because its work only 3.11 up versions. I recommend use timezone.utc, but risk to risk
        expires_delta = datetime.now(UTC) + timedelta(minutes=refresh_token)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(to_encode, jwt_refresh_key, algorithm)
