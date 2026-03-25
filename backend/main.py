from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, SQLModel
from models import User, UserOut
from database import engine, get_session
from users import get_current_user, router as users_router


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/Welcome", tags=["Welcome"])
async def Cyber():
    return {"Welcome to everyone"}
