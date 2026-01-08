# Repository Guidelines

## Project Structure & Module Organization

- `bradstarter/` is the main Python package, organized by domain (`admin/`, `auth/`, `items/`, `users/`, `general/`).
- Backend code lives under `bradstarter/general/backend/` with APIs in `bradstarter/**/backend/apis/`, shared components in `bradstarter/**/backend/components/`, and data models in `bradstarter/general/backend/data_models/`.
- Frontend code lives under `bradstarter/general/frontend/` with routes in `bradstarter/general/frontend/routes/`, UI in `bradstarter/general/frontend/elements/`, and assets in `bradstarter/general/frontend/public/`.
- Tests are colocated, typically `*_test.py` under `bradstarter/**/backend/`, plus frontend tests in `bradstarter/general/frontend/tests/` and Playwright configs at the repo root.

## Build, Test, and Development Commands

- `docker compose watch` starts the full local stack (backend, frontend, db, mailcatcher).
- `cd bradstarter/general/frontend && npm run dev` runs the Vite dev server on `http://localhost:5173`.
- `cd bradstarter/general/frontend && npm run build` builds the frontend for production.
- `bash bradstarter/general/backend/scripts/test.sh` runs backend pytest suite.
- `npx playwright test` runs Playwright end-to-end tests (requires Docker stack).
- `uv run pre-commit run --all-files` runs formatting/lint hooks.

## Coding Style & Naming Conventions

- Python: follow Ruff + Ruff-format (PEP 8, 4-space indents); use explicit typing and keep modules domain-scoped.
- Frontend: Biome handles lint/format; use double quotes and semicolons-as-needed per `biome.json`.
- Tests use `*_test.py` naming in backend; keep fixtures in `bradstarter/conftest.py` when shared.

## Testing Guidelines

- Backend tests use Pytest; run via `bradstarter/general/backend/scripts/test.sh`.
- Frontend E2E uses Playwright; ensure the Docker stack is running before `npx playwright test`.
- Coverage output is written to `htmlcov/` after backend tests.

## Commit & Pull Request Guidelines

- Recent commits use short, sentence-case summaries without prefixes (e.g., “Some fixes”).
- Keep commits focused; mention the domain being changed when possible.
- PRs should include a concise description, testing notes, and screenshots for UI changes. Link related issues when applicable.

## Security & Configuration Tips

- Update secrets in `.env` before running locally; avoid committing real credentials.
- Use `DOMAIN=localhost.tiangolo.com` in `.env` when testing subdomain routing.
