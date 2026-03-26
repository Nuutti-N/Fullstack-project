from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, SQLModel
from models import User, UserOut
from database import engine, get_session
from users import get_current_user, router as users_router


app = FastAPI()
app.include_router(users_router)


@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)
