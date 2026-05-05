---
name: model-creator
description: Generate domain models, entities, value objects, SQLAlchemy ORM models, migration files, and model unit tests following DDD and master-rules.
---

## Purpose

- Define robust domain models with clear boundaries.
- Generate pure Python domain entities and value objects.
- Generate SQLAlchemy ORM models for infrastructure persistence.
- Manage schema evolution through Alembic migrations.
- Ensure data integrity with comprehensive unit tests and validators.

## Required Outputs

- `app/{app_name}/domain/entities.py`: Pure Python business objects.
- `app/{app_name}/domain/value_objects.py`: Immutable objects representing descriptive aspects.
- `app/{app_name}/infrastructure/models.py`: SQLAlchemy ORM mappings.
- `pkg/validators/{field_name}.py`: Reusable validation logic if complex.
- Alembic migration file under `alembic/versions/`.
- `tests/unit/{app_name}/test_{model_name}.py`: Validation and behavior tests.

## Preflight

- Apply `.agent/skills/master-rules/SKILL.md`.
- Confirm the domain boundaries and model relationships.
- Check for existing validators in `pkg/validators/` to avoid duplication.

## Model Rules (DDD Alignment)

- **Standards**: Apply **Architecture Standards** from `master-rules`.
- **Domain Entities**: Use `@dataclass(kw_only=True)` for entities. Must include a `uid` field.
  - Entities must include an `update` method to handle state changes in a controlled manner.
- **Value Objects**: Use `@dataclass(frozen=True)` for value objects to ensure immutability.
- **Infrastructure Models**: Apply **Database (SQLAlchemy v2 & Alembic)** rules from `master-rules`.
  - Separation of Concerns: Domain entities must remain pure Python. Infrastructure models handle DB-specific mapping only.

## Validation & Code Style

- Apply **Documentation & Code Style** from `master-rules`.

## Implementation Details

- **Database**: Apply **Database (SQLAlchemy v2 & Alembic)** rules from `master-rules`.
- **Eager Loading**: Define relationships with appropriate loading strategies (`selectinload`, etc.) in infrastructure models.

## Documentation Rules

- Apply **In-Code Education & Documentation** and **Educational Document Structure** from `master-rules`.
- Explain the rationale behind the chosen value objects and entity structure.
- Provide examples of how to instantiate and use the models.

## Test Rules

- Create unit tests for domain behavior, `update` methods, and validation logic.
- Ensure ORM mapping is verified with repository or model-level tests.
- **Verification Loop**: Apply the **Verification Loop** and **Database (SQLAlchemy v2 & Alembic)** migration rules from `master-rules`.

## Git Workflow

- Apply the **Git Workflow** from `.agent/skills/master-rules/SKILL.md`.

## Finalization

- Apply the **Finalization Protocol** from `master-rules`.
