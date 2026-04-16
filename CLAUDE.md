# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trust AI Responses** — a tool that lets users paste AI-generated text or code and receive an instant trust analysis: a 0–100 trust score, verdict (`can use` / `let's explore more` / `do not use`), risks, pros, and a recommendation. Analysis is powered by Google Gemini and stored in Supabase.

## Commands

All commands run from the `MVP/` directory. The virtualenv is at the **repo root**, not inside `MVP/`.

```bash
# Activate virtualenv (Windows) — run from repo root (C:\CYBER AI)
venv\Scripts\activate

# Run dev server (from MVP/)
fastapi dev backend/main.py
# or
uvicorn backend.main:app --reload

# Run all tests
pytest

# Run a single test file
pytest backend/tests/test_routers.py

# Run a single test by name
pytest backend/tests/test_routers.py::test_welcome

# Lint and format (dev dependencies in pyproject.toml)
black .
ruff check .

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

The API runs at `http://localhost:8000`. Interactive docs at `/docs`.

## Environment Variables

Create `backend/.env` with:

```env
DATABASE_URL=your_postgres_url
JWT_KEY=your_jwt_secret
JWT_REFRESH_KEY=your_jwt_refresh_secret
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_service_role_key
GEMINI_API_KEY=your_gemini_api_key
```

Supabase key: use the **anon key** if RLS is enabled on tables, **service role key** if RLS is disabled.

## Architecture

```
MVP/
├── backend/
│   ├── main.py             # FastAPI app, CORS, rate-limit error handler, router registration
│   ├── config.py           # Pydantic Settings — loads .env, fails fast if any var missing
│   ├── models.py           # SQLModel table: User; Pydantic schemas: UserAuth, UserOut, Token, TokenPayload, SystemUser
│   ├── database.py         # SQLAlchemy engine (echo=True — logs all SQL); get_session() dependency
│   ├── users.py            # /signup, /login, /your, /refresh endpoints + get_current_user() JWT dependency
│   ├── routers.py          # /welcome, /chat, /analyze, /history, /delete_history/* endpoints
│   ├── utils.py            # bcrypt hashing, JWT access/refresh token creation (30 min / 7 days)
│   ├── supabase_client.py  # Supabase client singleton
│   ├── rating_limiter.py   # slowapi Limiter instance (key: remote IP)
│   ├── logger.py           # Shared logger — INFO to console, DEBUG to app.log file
│   └── alembic/            # DB migrations (targets SQLModel metadata only)
└── Frontend/               # React frontend — not yet implemented
```

### Request flow for `/analyze`

1. Rate limiter checks `5/minute` per IP.
2. `get_current_user()` decodes the Bearer JWT and resolves to a `User` row from Postgres.
3. A structured prompt is sent to Gemini asking for JSON with `trust_score`, `verdict`, `risks`, `pros`, `recommend`.
4. The raw response is parsed with `json.loads` after stripping markdown fences — Gemini sometimes wraps JSON in ` ```json ``` `.
5. Result is inserted into Supabase `fact_checks` table (`user_id`, `claim`, `answer` only — full analysis is not persisted).
6. Full analysis object is returned to the caller.

### Auth flow

- `POST /signup` — hashes password with bcrypt, stores `User` in Postgres.
- `POST /login` — verifies bcrypt, returns `{access_token, refresh_token}` (JWT HS256).
- `POST /refresh` — validates refresh token, issues a new token pair.
- All protected endpoints use `get_current_user()` as a FastAPI `Depends`, which decodes the Bearer JWT against `JWT_KEY`.
- JWT `sub` field stores the **username** (not user ID).

### Dual database usage

The app uses two separate data stores intentionally:
- **SQLModel/SQLAlchemy (Postgres)** — `User` table only, managed via Alembic migrations.
- **Supabase client (PostgREST)** — `fact_checks` table, accessed via the Supabase Python SDK. This table is **not** in SQLModel metadata and is **not** managed by Alembic.

### Tests

Tests use SQLite (`sqlite:///test.db`) set via `conftest.py` env override and `fastapi.testclient.TestClient`. The `clean_test_db` fixture drops and recreates all SQLModel tables around each test.

**Important:** Supabase calls are **not mocked** — tests hitting `/analyze` or `/history` make real network requests to Supabase unless patched manually.

Config is loaded at module import time via `settings = Settings()` in `config.py`. The `set_mock_env` fixture is `scope="session"` so env vars must be set before any backend module is imported.

### Deployment

A `Procfile` is present for Heroku/Railway:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

`echo=True` in `database.py` logs every SQL statement — disable this before deploying to production.
