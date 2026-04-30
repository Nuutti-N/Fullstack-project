from fastapi.middleware.cors import CORSMiddleware
from backend.logger import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.users import router as users_router
from backend.routers import router as routers
from backend.health import router as health
from slowapi.errors import RateLimitExceeded
from backend.rate_limiter import limiter
from contextlib import asynccontextmanager
from backend.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


app = FastAPI(lifespan=lifespan)


# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        # "https://fullstack-project-nine-chi.vercel.app"

    ],
    allow_credentials=True,
    allow_methods=["GET", "DELETE", "POST"],
    allow_headers=["Content-Type", "Authorization"]
)

app.include_router(users_router)
app.include_router(routers)
app.include_router(health)

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many request. Please slow down and try again later."}
    )
