---
name: model-creator
description: Create GORM models and SQL migrations. **MANDATORY** ALWAYS read .agent/skills/references/backend/RULES.md before implementation.
---

# Context
**CRITICAL**: You MUST read and strictly follow [Backend Rules](../../references/backend/RULES.md) before starting any task. Every decision (naming, fields, migrations) must align with these rules.

# Requirements
- Fields: ID (BIGINT AUTO_INCREMENT PK), UID (ULID, index), timestamps (DATETIME created_at/updated_at).
- Tags: `json`, `gorm`, `validate`.
- Migrations: `internal/migrations/` using `gormigrate` v2 and raw MariaDB/MySQL SQL (`IF NOT EXISTS`).

# Implementation
1. Add model to `internal/models/`.
2. Create migration file with prefix `00X_`.
3. Register migration in bootstrap.
