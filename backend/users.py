from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import datetime
from jose import jwt, JWTError
from database import engine
from Models import (
    UserOut,
    UserAuth,
    User,
    token,
)
from utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenurl="token")


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/Signup", response_model=UserOut, tags=["Sign up"])
async def register(data: UserAuth, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == data.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username exists")
    hashed_pass = hash_password(data.password)
    new_user = User(username=data.username, password=hashed_pass)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/Login", response_model=token, tags=["login"])
async def Login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    existing_user = session.exec(statement).first()
    if existing_user is None:
        raise HTTPException(
            status_code=401, detail="Incorrect Username or password")
    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    return {
        "acces_token": create_access_token(existing_user.username),
        "refresh_token": create_refresh_token(existing_user.username)
    }
reuseable_oauth = OAuth2PasswordBearer(
    tokenURL="/Login",
    scheme_name="JWT"
)
