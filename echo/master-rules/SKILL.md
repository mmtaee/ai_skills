---
name: master-rules
description: Unified global rules for the agent, covering baseline architecture, implementation standards, documentation, and educational content.
---

## Core Philosophy

- **Cloud Native**: All projects must be designed for cloud environments. This means configuration via environment variables is mandatory, services must be stateless, and infrastructure should be container-ready.
- **Thorough Preflight**: Never start a task without reviewing all relevant skill definitions in `.agent/skills/`.
- **Absolute Quality**: Code must be clean, typed, documented, and validated with `pre-commit` and tests.
- **Educational Value**: Every output should help the user learn the "why" and "how" of the implementation.

## Preflight Checklist

1. **Review Skill**: Read the relevant project or logic-specific `SKILL.md` file.
2. **Context Gathering**: Search the codebase for existing patterns, helpers, and dependencies before proposing new ones.
3. **Requirement Check**: Confirm the requested output type (scaffold, logic, doc) and scope.

## Documentation & Code Style

- **Type Hints**: Mandatory for all variables, function arguments, and return types.
- **Unique Identifiers**:
  - For **Request IDs** (X-Request-Id) and ephemeral tracing: Always use **CUID** (specifically `cuid2`).
  - For **Model UIDs**, persistent identifiers in the database: Always use **ULID**. Never use standard UUIDs or CUIDs.
- **Validators**: All reusable validation logic must reside in `pkg/validators/`. Each validator must be in its own dedicated file. Validators should be modular, testable, and follow a consistent naming convention (e.g., `phone_validator`).
- **In-Code Education**:
  - Add brief comments to complex logic.
  - Explain the "why" behind specific architectural choices.
  - Use docstrings for modules, classes, and complex functions with `Args`, `Returns`, and `Example`.

- **Coding Best Practices**:
  - **Static Methods**: If a class method does not use `self`, it MUST be decorated with `@staticmethod`.
  - **Authentication**: Prefer using FastAPI **Dependencies** (e.g., `Depends(get_current_user)`) for authentication and user existence checks rather than manual logic inside endpoints.
  - **Error Handling**: Use consistent, snake_case error strings in `HTTPException` detail (e.g., `invalid_token`, `user_not_found`).

- **Absolute Imports**: Always use absolute paths (e.g., `from pkg.decorators import rate_limit`) instead of relative dots.
- **Naming**: Use PascalCase for classes, snake_case for attributes and files.
- **API Documentation**:
  - All endpoints with rate limiting MUST explicitly document the `429 Too Many Requests` response.
  - The description MUST include the specific limits (e.g., `3/m, 5/h`) so they are visible in Swagger/Redoc.
- **Type Hints**: Mandatory for all variables, function arguments, and return types.
- **Verification Loop**: After significant changes, you MUST:
  1. Run formatting tools (`black`).
  2. Run linting/pre-commit hooks (`pre-commit run --all-files`).
  3. Execute unit/integration tests (`pytest`).
  4. Run Robot Framework tests if applicable (`robot --console dotted`).

## Architecture Standards (DDD & Clean Architecture)

- **Presentation Layer**: Thin FastAPI routes; delegate all logic to the application layer.
- **Application Layer**: Orchestrate business logic using use cases; inject repositories for persistence.
- **Domain Layer**: Pure Python entities and services; use `dataclasses` for domain objects.
- **Infrastructure Layer**: Handle persistence, Redis, and external APIs; keep this layer decoupled from business rules.
- **Absolute Imports**: Enforce across all layers.

## Implementation Rules (Database & Redis)

- Follow the application structure: `Presentation → Application → Domain → Infrastructure`.
- Use a dedicated directory for each project under `app/` (e.g., `app/{app_name}/`).

### Database (SQLAlchemy v2 & Alembic)
- Use `Mapped` and `mapped_column` for all models.
- Use `CustomBaseModel` or `CustomBaseModelTimestamp` from `pkg/shared/models.py`.
- **Eager Loading**: Prevent N+1 issues using `selectinload`, `joinedload`, or `subqueryload`.
- **Transactions**: Use unit-of-work boundaries in repositories.
- **Initialization**: In `alembic/env.py`, set `target_metadata = CustomBaseModel.metadata`. Use `# noqa: F401` for registration-only imports.
- **Migrations**: After every model creation or update, you MUST automatically run:
  1. `alembic revision --autogenerate -m "create or update {model_name} models"`
  2. Apply migrations to the database (`alembic upgrade head`).
- **No SQLite**: Always assume a production-ready DB like MariaDB; construct `DATABASE_URL` dynamically in `config/settings.py`.

### Redis
- **Modular Package**: Keep all Redis logic in `pkg/redis/` (e.g., `client.py`, `lock.py`).
- **Async Operations**: All Redis operations MUST be asynchronous. You MUST `await` all coroutines (e.g., `await redis.get(key)`, `await redis.client.incr(key)`).
- **Serialization**: Use JSON with an explicit interface.
- **Distributed Locks**: Use `CacheLock` for concurrency control.
- **Lifecycle**: Manage `init_redis` and `get_redis` in `config/redis.py`.

## In-Code Education & Documentation

To ensure the codebase is accessible to new developers and maintainers, every file must include educational context:
- **Module-Level Docstrings**: Every Python file must start with a docstring explaining its purpose, its role in the DDD/Clean Architecture, and how it interacts with other components.
- **Structural Comments**: Use comments to explain "why" a specific architectural choice was made, not just "what" the code does.
- **Complexity Guidance**: For non-trivial logic (e.g., custom decorators, complex SQL queries, or Redis locks), provide a brief explanation of the underlying concept.
- **Reference Links**: Where applicable, include references to the relevant `SKILL.md` or external documentation.

## Educational Document Structure

When generating documentation, READMEs, or educational insights:
- **Learning Objectives**: Start with what the user will achieve.
- **Readability**: Use clear headers, subheadings, and numbered steps.
- **Examples**: Include minimal, correct, and relevant code snippets or analogies.
- **Exercises**: Provide review questions or practical tasks for the user.
- **Summaries**: End with a concise recap and "Next Steps" guidance.

## Git Workflow (MANDATORY)

If a `.git` directory exists in the project root, every skill MUST follow this workflow:
1. **Confirmation**: Ask the user for confirmation (Yes/No) before staging any changes.
2. **Commitizen**: Use **Commitizen** (`cz commit` or `uv run cz commit`) for all commits to ensure **Conventional Commits** compliance.
3. **No Push**: Never perform `git push`. Only local commits are permitted.
4. **Interactive**: Prefer the interactive `cz commit` prompts to ensure high-quality, standardized commit messages.

## Finalization Protocol

Before handing back to the user:
1. **Format**: Run `black` on all modified files.
2. **Lint**: Execute `pre-commit run --all-files`.
3. **Test**: Run `pytest` and Robot Framework tests where applicable.
4. **Document**: Ensure all new/modified code has docstrings and type hints.
5. **Verify**: Ensure the `main.py` server is ready or the requested logic is fully functional.
