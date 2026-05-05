---
name: project-creator
description: Generate an efficient, human-friendly FastAPI backend scaffold using DDD, Clean Architecture, Redis, and SQLAlchemy.
---

## Purpose

- Generate a complete backend project scaffold in the project root directory.
- Create a project structure following best practices.
- No need to create a project-named directory; use existing root.
- Implement common features like rate limiting, request mutex, idempotency, request ID injection, structured logging, and error handling.
- Use Redis for caching and message broker (optional).
- Use SQLAlchemy for database operations.
- Follow shared rules, documentation style, and Redis/Database safeguards.
- Use prompt-efficient wording to minimize token cost and improve clarity.

## Prompt Efficiency

- Use short, direct sentences.
- Avoid repeated statements.
- Prefer bullet lists over long paragraphs.
- Refer to shared skill files instead of restating the same rules.
- Keep output structure predictable and easy to scan.

## Dependencies

- UV
- Python >= 3.13
- FastAPI, Uvicorn, Alembic, SQLAlchemy v2
- MariaDB:11, Redis:8
- Black, commitizen, pre-commit, pytest, coverage, robot framework

## Preflight

- Apply `.agent/skills/master-rules/SKILL.md`.
- Confirm the task is backend scaffold generation, not an isolated script.
- Detect whether the workspace already contains an existing `pkg/` service package for the requested application.

## Project Structure
  ./
    app/ # dont create any application package under this dir.
    pkg/
      __init__.py
      middlewares/
      decorators/
      validators/
      auth/
        __init__.py
        jwt.py
        dependencies.py
      s3/
      redis/
      utils/
      shared/
        models.py
    scripts/
      run.sh, coverage.sh, run_test.sh
    alembic/, config/, tests/
    pyproject.toml, README.md, .pre-commit-config.yaml, .env.sample, docker-compose.yml, Dockerfile, .gitlab-ci.yml, .coveragerc, .gitignore

## Creation Rules

- Apply **Documentation & Code Style** and **In-Code Education** rules from `master-rules`.
- Copy configuration files (`.dockerignore`, `.gitignore`, `.pre-commit-config.yaml`, `models.py`, `rate_limit.py`, `cache.py`) from `.agent/skills/project-creator/configs/`.
- **Infrastructure Configuration**:
  - `config/settings.py`: Construct `DATABASE_URL` dynamically from environment variables using `pydantic-settings`. Settings must be **Cloud Native**: prioritize OS environment variables and only use `.env` files as an optional fallback for local development.
  - `config/database.py`: SQLAlchemy engine and session management.
  - `config/cache.py`: Redis client lifecycle (renamed to avoid shadowing the redis library).
  - `config/s3.py`: S3 client lifecycle.
- Apply **Architecture Standards** from `master-rules`.

## Architecture Rules

- Apply **Architecture Standards (DDD & Clean Architecture)** from `master-rules`.
- Use **RustFS** as the default S3-compatible object storage in `docker-compose.yml`.

## Documentation Rules

- Apply **Educational Document Structure** from `master-rules`.

## FastAPI Rules

- Configure `main.py` with `custom_openapi`, `lifespan`, and routers.
- Add health/readiness endpoints.
- Use structured JSON logging.
- Add middleware for request ID, tracing, and error handling.

## Required Modules

- **Decorators**: `pkg/decorators/` (rate_limit, mutex).
- **Middlewares**: `pkg/middlewares/` (request_id, tracing, error_handler).
  - Create Middleware for structured request/response/error tracing in `pkg/middlewares/tracing.py`.
    - Minimum JSON fields: request headers, request body, request method, X-Request-Id, response headers, response body, error, private error hint, file/line trace, status code.
    - Allow extra fields when needed.
- **Auth**: `pkg/auth/` (jwt, dependencies).
  - Implement **JWT Token Strategy** in `pkg/auth/jwt.py`.
  - JWT must support a **claims type** (extensible dictionary) to allow adding custom fields to the token payload.
  - Include token generation (`encode`) and validation/decoding (`decode`) logic.
- **Validators**: `pkg/validators/` (standard naming, one file per validator).
- **Redis & S3**: `pkg/redis/`, `pkg/s3/` (operational client wrappers).
- **Shared**: `pkg/shared/schemas.py` (Error400).
- **Testing**: `tests/unit/`, `tests/integration/`, `tests/robot/`.
- **Scripts**: `scripts/run.sh`, `scripts/run_test.sh`, `scripts/coverage.sh`.

## Redis and Database Guidance

- Apply **Implementation Rules (Database & Redis)** from `master-rules`.

## Git Workflow
}
- Apply the **Git Workflow** from `master-rules`.

## Finalization

- Apply the **Finalization Protocol** from `master-rules`.
- Initialize **Commitizen** in `pyproject.toml`.
- Use `pyproject.toml` for all dependencies.
