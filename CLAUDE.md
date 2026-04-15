# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trust AI Responses** — a tool that lets users paste AI-generated text or code and receive an instant trust analysis: a 0–100 trust score, verdict (`can use` / `let's explore more` / `do not use`), risks, pros, and a recommendation. Analysis is powered by Google Gemini and stored in Supabase.

## Commands

All commands run from the `MVP/` directory with the venv activated.

```bash
# Activate virtualenv (Windows)
venv\Scripts\activate

# Run dev server (from MVP/)
fastapi dev backend/main.py
# or
uvicorn backend.main:app --reload

# Run all tests
pytest

# Run a single test file
pytest backend/tests/test_routers.py

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
│   ├── main.py          # FastAPI app, CORS, rate-limit error handler, router registration
│   ├── config.py        # Pydantic Settings — loads .env, fails fast if any var missing
│   ├── models.py        # SQLModel table: User; Pydantic schemas: UserAuth, UserOut, token, TokenPayLoad, SystemUser
│   ├── database.py      # SQLAlchemy engine from settings.database_url; get_session() dependency
│   ├── users.py         # /signup, /login, /your endpoints + get_current_user() JWT dependency
│   ├── routers.py       # /welcome, /chat, /analyze, /history, /delete_history/* endpoints
│   ├── utils.py         # bcrypt hashing, JWT access/refresh token creation (30 min / 7 days)
│   ├── supabase_client.py  # Supabase client singleton
│   ├── rating_limiter.py   # slowapi Limiter instance (key: remote IP)
│   ├── logger.py        # Shared logger
│   └── alembic/         # DB migrations (targets SQLModel metadata)
└── Frontend/            # React frontend — not yet implemented
```

### Request flow for `/analyze`

1. Request hits rate limiter (`5/minute` per IP via `@limiter.limit`).
2. `get_current_user()` validates the JWT Bearer token and resolves to a `User` row.
3. A structured prompt is sent to Gemini (`gemini-3-flash-preview`) asking for JSON with `trust_score`, `verdict`, `risks`, `pros`, `recommend`.
4. The raw JSON string from Gemini is parsed with `json.loads` — if Gemini returns non-JSON, this raises an unhandled exception.
5. The result is inserted into the Supabase `fact_checks` table (`user_id`, `claim`, `answer`).
6. The full analysis object is returned to the caller.

### Auth flow

- `POST /signup` — hashes password with bcrypt, stores `User` in Postgres.
- `POST /login` — verifies bcrypt, returns `{access_token, refresh_token}` (JWT HS256).
- All protected endpoints use `get_current_user()` as a FastAPI `Depends`, which decodes the Bearer JWT against `JWT_KEY`.

### Dual database usage

The app uses **two separate data stores**:
- **SQLModel/SQLAlchemy (Postgres)** — `User` table, managed via Alembic migrations.
- **Supabase client (PostgREST)** — `fact_checks` table, accessed via the Supabase Python SDK. This table is not in SQLModel metadata and is not managed by Alembic.

### Tests

Tests use SQLite in-memory (set via `conftest.py` env override) and `fastapi.testclient.TestClient`. The `clean_test_db` fixture drops and recreates all SQLModel tables around each test. Supabase calls are **not** mocked — tests that hit `/analyze` or `/history` will attempt real Supabase requests unless patched.
