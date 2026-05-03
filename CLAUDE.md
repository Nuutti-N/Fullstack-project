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

# Lint and format
black .
ruff check .

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Frontend dev server (from MVP/frontend/app/)
npm run dev
```

The API runs at `http://localhost:8000`. Interactive docs at `/docs`.
Frontend dev server runs at `http://localhost:5173`.

## Environment Variables

`backend/.env`:

```env
DATABASE_URL=your_postgres_url
JWT_KEY=your_jwt_secret
JWT_REFRESH_KEY=your_jwt_refresh_secret
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_service_role_key
GEMINI_API_KEY=your_gemini_api_key
```

`frontend/app/.env`:

```env
VITE_API_URL=http://localhost:8000
```

Supabase key: use the **anon key** if RLS is enabled, **service role key** if RLS is disabled.

## Architecture

```
MVP/
├── backend/
│   ├── main.py             # FastAPI app, CORS, rate-limit error handler, router registration
│   ├── config.py           # Pydantic Settings — loads .env, fails fast if any var missing
│   ├── models.py           # SQLModel table: User; Pydantic schemas: UserAuth, UserOut, Token, TokenPayload, SystemUser, HealthCheck
│   ├── database.py         # SQLAlchemy engine; get_session() dependency
│   ├── users.py            # /signup, /login, /your, /refresh endpoints + get_current_user() JWT dependency
│   ├── routers.py          # /welcome, /chat, /analyze, /history, /delete_history/{id}, /delete_all_history/ endpoints
│   ├── health.py           # /health endpoint — returns {"status": "OK"}
│   ├── utils.py            # bcrypt hashing, JWT access/refresh token creation (30 min / 7 days)
│   ├── supabase_client.py  # Supabase client singleton
│   ├── rate_limiter.py     # slowapi Limiter instance (key: remote IP)
│   ├── logger.py           # Shared logger — INFO to console, DEBUG to app.log file
│   └── alembic/            # DB migrations (targets SQLModel metadata only)
└── frontend/
    └── app/                # Vite + React app
        ├── src/
        │   ├── pages/
        │   │   ├── Login.jsx     # ✅ Done — styled, error state, show/hide password, link to signup
        │   │   ├── Signup.jsx    # ✅ Done — styled, error state, show/hide password, link to login
        │   │   ├── Analyze.jsx   #  ✅ Done Working but UNSTYLED — raw form, no CSS classes
        │   │   ├── home.jsx      # ✅ Done — hero section with CTA buttons
        │   │   └── home.css
        │   ├── components/
        │   │   ├── PrivateRoutes.jsx        # ✅ Done — checks localStorage token, redirects to /login
        │   │   └── Navbar/
        │   │       ├── NavBar.jsx           # ✅ Has React hooks bug — see Known Issues
        │   │       └── NavBar.css
        │   ├── api/
        │   │   └── client.js     # ✅ Done — axios instance with baseURL + Bearer token interceptor
        │   ├── App.jsx           # ✅ Done — BrowserRouter + NavBar + PrivateRoute + all Routes
        │   ├── App.css
        │   └── main.jsx
        ├── public/
        │   ├── favicon.svg
        │   └── icons.svg
        └── package.json
```

### Request flow for `/analyze`

1. Rate limiter checks `1/minute` per IP.
2. `get_current_user()` decodes the Bearer JWT and resolves to a `User` row from Postgres.
3. Instructions are sent via `system_instruction`, user text via `contents` — separated to prevent prompt injection.
4. Gemini returns JSON directly (`response_mime_type="application/json"`), parsed with `json.loads`.
5. Result is inserted into Supabase `fact_checks` table.
6. Full analysis object is returned to the caller.

### Auth flow

- `POST /signup` — hashes password with bcrypt, stores `User` in Postgres.
- `POST /login` — verifies bcrypt, returns `{access_token, refresh_token}` (JWT HS256).
- `POST /refresh` — validates refresh token, issues a new token pair.
- All protected endpoints use `get_current_user()` as a FastAPI `Depends`, which decodes the Bearer JWT against `JWT_KEY`.
- JWT `sub` field stores the **user ID** (integer, converted to string in token).

### Dual database usage

- **SQLModel/SQLAlchemy (Postgres)** — `User` table only, managed via Alembic migrations.
- **Supabase client (PostgREST)** — `fact_checks` table, accessed via the Supabase Python SDK. Not in SQLModel metadata, not managed by Alembic.

### Tests

Tests use SQLite (`sqlite:///test.db`) set via `conftest.py` env override and `fastapi.testclient.TestClient`. The `clean_test_db` fixture drops and recreates all SQLModel tables around each test.

**Coverage:**
- `test_user.py` — signup, login, login failure, `/your` with and without token
- `test_routers.py` — `/welcome`, auth guards on all protected endpoints, `/your` and `/refresh` with valid token
- `test_database.py` — database-level tests

**Important:** Supabase calls are **not mocked** — tests hitting `/analyze`, `/history`, or `/delete_history` make real network requests to Supabase unless patched manually.

### Deployment

`Procfile` for Heroku/Railway:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

`frontend/app/vercel.json` — frontend deploys to Vercel.

`Dockerfile` + `docker-compose.yml` — containerised setup available.

## Frontend Teaching Progress

The user is learning React step-by-step. Do not write frontend code for them — explain, let them write, then review.

**Completed lessons:**
- ✅ Lesson 1 — React Router: `<BrowserRouter>`, `<Routes>`, `<Route>`. User wrote 3 Route entries in App.jsx.
- ✅ Lesson 2 — Login page: `useState` for username + password, controlled inputs, form + submit button, `async handleSubmit` with `e.preventDefault()`.
- ✅ Lesson 3 — Login API call: `api.post()`, `await`, `URLSearchParams` for form-urlencoded, CORS debugging. Got tokens in console.
- ✅ Lesson 4 — Finish Login: `localStorage.setItem("token", ...)` + `useNavigate` redirect.
- ✅ Lesson 5 — Signup page: same shape as Login, hits `POST /signup`, redirects to `/login`.
- ✅ Lesson 6 — Analyze page: textarea + `POST /analyze` + render trust score/verdict/risks/pros/recommend.
- ✅ Lesson 7 — History page: `useEffect` + `GET /history` on mount, list results.
- ✅ Lesson 8 — `PrivateRoute.jsx`: protects `/analyze` and `/history`, redirects unauthenticated users.
- ✅ Lesson 9 — Fixed `'bearer' + token` → `'Bearer ' + token` (capital B + space) in `api/client.js`.
- ✅ Lesson 10 — Styling: login.css applied to Login and Signup. Home page hero section styled.
- ✅ Lesson 11 — Logout + show current user: NavBar calls `GET /your`, displays username, has logout button.
- ✅ Lesson 12 — NavBar: hides itself on `/login` and `/signup` routes using `useLocation`.
- ✅ Lesson 13 - Analyze, results use class, what I polish in analyze.css. Results is understandable

**Current state (as of 2026-05-02):**
- Login ✅ Styled and complete.
- Signup ✅ Styled and complete.
- Home ✅ Hero section done.
- Analyze ✅ Functional + styled (card, buttons, textarea). History slide panel complete (open/close, overlay, delete, empty state, header with count). Results card still unstyled.
- NavBar ✅ Complete.
- Chat page — decided NOT to build. Out of scope for MVP.

**Concepts learned (as of 2026-05-02):**
- Boolean state for show/hide (`showHistory` true/false)
- Dynamic className with ternary
- JSX curly braces `{}` — JavaScript inside JSX needs `{}`
- `key` prop goes on the outer div of each list item
- Setter vs value (`showHistory` = value, `setShowHistory` = function)
- CSS slide panel: `position: fixed`, `transform: translateX`, `transition`
- `z-index`: controls which element appears on top
- Overlay pattern: dark semi-transparent layer, `onClick` closes the panel
- Empty state message: `{array.length === 0 && <p>...</p>}`

**Next (final 2 tasks to ship MVP):**
- 🔜 Click history item → load its result into the results section

**Teaching style reminders:**
 KEEP MESSAGES VERY SHORT (~10 lines max). Numbered steps. Simple words.
- ONE new concept per turn.
- Always link to official docs (MDN, react.dev, axios-http.com).
- Never write code for them. Guide; let them type it.
- you are a senior developer, and your task to teach beginner level.

## Known Issues & Gotchas


### Security

- `DELETE /delete_all_history/` permanently deletes all of a user's records with no confirmation. Consider requiring a body param like `{"confirm": true}` before shipping.

### Tests

- Supabase is not mocked. Any test calling `/analyze`, `/history`, or `/delete_history` makes real HTTP requests to Supabase and will fail without live credentials.
- No test covers a full successful `/analyze` flow (would need Supabase mock + Gemini mock).

### Production Readiness

- CORS `allow_origins` hardcodes `localhost` URLs — add the production frontend URL (e.g. Vercel domain) before deploying.
- `settings.VITE_API_URL` is commented out in CORS origins in `main.py` — uncomment and wire up for production.

