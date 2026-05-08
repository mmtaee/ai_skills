---
name: project-creator
description: Initialize or update the project structure. **MANDATORY** ALWAYS read .agent/skills/references/backend/RULES.md before implementation.
---

# Context
**CRITICAL**: You MUST read and strictly follow [Backend Rules](../../references/backend/RULES.md) before starting any task. Every decision (naming, directories, patterns) must align with these rules.

# Stack
- Framework: Echo v5.
- DB: GORM (MariaDB stable default).
- CLI: Cobra.
- Migrations: Gormigrate v2.
- Validation: Validator v10.

# Structure
- `cmd/`: CLI commands (root, serve, docs).
- `internal/`: Business logic (service, repository, usecase).
- `pkg/`: Shared modules (bootstrap, routing, middlewares, request).
- `config/`: Configuration and `errors.json`.

# Bootstrapping
1. Init go mod.
2. Setup directory structure.
3. Implement core middleware (CORS, Logger, Timeout, RateLimit).
4. Configure DB connection and migrations.
