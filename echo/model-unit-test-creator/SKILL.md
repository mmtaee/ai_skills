---
name: model-unit-test-creator
description: Create unit tests for GORM models. **MANDATORY** ALWAYS read .agent/skills/references/backend/RULES.md before implementation.
---

# Context
**CRITICAL**: You MUST read and strictly follow [Backend Rules](../../references/backend/RULES.md) before starting any task. Every decision (naming, structure, helpers) must align with these rules.

# Standards
- Path: `internal/models/tests/model_name_test.go`.
- Package: `tests`.
- Helper: Use `pkg/testutils` for DB setup.
- Coverage: CRUD operations and status changes.

# Tasks
1. Create/update test file.
2. Ensure database cleanup/setup per test.
3. Verify with `go test ./...`.
