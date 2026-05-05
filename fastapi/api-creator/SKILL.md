---
name: api-creator
description: Generate API-layer modules, FastAPI endpoints, and comprehensive tests (unit, integration, robot) within a DDD/Clean Architecture application.
---

## Purpose

- Generate FastAPI endpoints and presentation layer logic.
- Create request/response schemas and dependency providers.
- Implement comprehensive automated testing for every API.

## Preflight

- Apply `.agent/skills/master-rules/SKILL.md`.
- **App Name Requirement**: The `app_name` is mandatory. If not provided by the user, you MUST ask for it before proceeding.
- Detect existing app structure in `app/{app_name}/`.

## API Creation Rules

- **Directory Structure**: Create APIs within their own app directory:
  - `app/{app_name}/presentation/api.py`: Route definitions and handlers.
  - `app/{app_name}/presentation/schemas.py`: Pydantic request/response models.
- **Standards**:
  - Apply **Documentation & Code Style** and **Architecture Standards** from `master-rules`.
  - Endpoint handlers must remain thin, delegating all business logic to the application layer.
  - **Response Schemas**: Each API endpoint MUST have its own dedicated response schema defined in `schemas.py`.
  - **Schema Structure**: Responses should directly return the domain object or data, wrapped in a descriptive key if necessary (e.g., `user: {...}`).
  - **Inheritance**: Use inheritance for common response patterns (e.g., an `AuthResponse` that includes a `UserResponse`).
  - **No Generic Wrapper**: Do NOT use a generic `BaseResponse` wrapper (like `{"status": "success", "data": ...}`).
  - **Empty Responses**: Responses with status codes `202 Accepted` or `204 No Content` MUST NOT include a response body or message.

## Testing Rules

For every API created, you MUST implement the following tests:

1. **Unit Tests**:
   - Location: `app/{app_name}/tests/unit/test_api.py`
   - Purpose: Test individual endpoint logic with mocked dependencies.
2. **Integration Tests**:
   - Location: `app/{app_name}/tests/integration/test_api.py`
   - Purpose: Test the interaction between the API and infrastructure (DB, Redis, S3).
3. **Robot Framework Tests**:
   - Location: `tests/robot/{app_name}/`
   - Purpose: End-to-end acceptance tests based on the user-provided scenario.
   - Requirement: Ask the user for specific test scenarios if not provided.

## Verification Loop

- Apply the **Verification Loop** from `.agent/skills/master-rules/SKILL.md`.

## Git Workflow

- Apply the **Git Workflow** from `.agent/skills/master-rules/SKILL.md`.
