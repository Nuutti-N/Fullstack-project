from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, SQLModel
from backend.models import User, UserOut
from backend.database import engine, get_session
from backend.users import get_current_user, router as users_router
from backend.routers import router as routers

app = FastAPI()
app.include_router(users_router)
app.include_router(routers)


@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)
