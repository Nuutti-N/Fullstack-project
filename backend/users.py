from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import ValidationError
from datetime import datetime, timezone
from jose import jwt, JWTError
from backend.database import engine
from backend.models import (
    UserOut,
    UserAuth,
    User,
    token,
    TokenPayLoad,
    SystemUser
)
from backend.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    jwt_key,
    algorithm
)
from backend.logger import logger

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/Signup", response_model=UserOut, tags=["Sign up"])
async def register(data: UserAuth, session: Session = Depends(get_session)):
    try:
        statement = select(User).where(User.username == data.username)
        existing_user = session.exec(statement).first()
        if existing_user:
            logger.warning(
                f"Sign up attempt with existing username: {data.username}")
            raise HTTPException(status_code=400, detail="Username exists")
        hashed_pass = hash_password(data.password)
        new_user = User(username=data.username, password=hashed_pass)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        logger.info(f"New user registered: {data.username}")
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/Login", response_model=token, tags=["Login"])
async def Login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    existing_user = session.exec(statement).first()
    if existing_user is None:
        logger.warning(
            f"Failed Login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=401, detail="Incorrect Username or password")
    if not verify_password(form_data.password, existing_user.password):
        logger.warning(f"Wrong password for username: {form_data.username}")
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    logger.info(f"User Logged in: {form_data.username}")
    return {
        "access_token": create_access_token(existing_user.username),
        "refresh_token": create_refresh_token(existing_user.username)
    }
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/Login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth), session: Session = Depends(get_session)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, jwt_key, algorithms=[algorithm]
        )
        token_data = TokenPayLoad(**payload)
        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired", headers={
                "WWW-Authenticate": "Bearer"
            })
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials", headers={
            "WWW-Authenticate": "Bearer"
        })

    statement = select(User).where(User.username == token_data.sub)
    new_user = session.exec(statement).first()
    if new_user is None:
        raise HTTPException(status_code=400, detail="Could not find user")
    return new_user


@router.get("/Your", summary="Get details of currently logged in user", response_model=UserOut, tags=["Login information"])
async def get_mer(user: User = Depends(get_current_user)):
    return user
