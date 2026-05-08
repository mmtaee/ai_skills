---
name: api-creator
description: Create Echo v5 APIs using Service/Repository/Usecase pattern. 
  **MANDATORY** ALWAYS read .agent/skills/references/backend/RULES.md before implementation.
---

# Context
**CRITICAL**: You MUST read and strictly follow [Backend Rules](../../references/backend/RULES.md) before starting any task. Every decision (naming, structure, errors, pagination) must align with these rules.

# Strategy
- Service: `internal/service/{name}/` (controller.go, routes.go, types.go).
- Validation: Use `request.Validator` and `request.BadRequest`.
- Logic: Use `ResponseWithCode` for `config/errors.json` keys, or `BadRequest` for system errors.
- Documentation: Add Swagger comments and run `swag init --pd`.

# Workflow
1. Define request/response structs in `types.go`.
2. Implement controller logic with validation.
3. Register routes in service and aggregate in `internal/provider/routes.go`.
4. Update Swagger docs.

# Note:
- Note:
- instead of using `// @Security ApiKeyAuth` in swagger use:
```text
// @Param        Authorization header string true "Bearer TOKEN"
// @Failure 401 {object} request.ErrorResponse
```
- for pagination use pkg/request/pagination module 
- for separate swagger documentation:
  - use separate directories in `docs/` (e.g., `docs/client`, `docs/admin`).
  - use separate provider sub-packages (e.g., `internal/provider/client`, `internal/provider/admin`).
  - generate in `api/` directory with:
    - Client: `swag init -g internal/provider/client/routes.go --exclude ./internal/service/admin --instanceName client -o ./docs/client --pd`
    - Admin: `swag init -g internal/provider/admin/routes.go --exclude ./internal/service/client --instanceName admin -o ./docs/admin --pd`
  - serve each documentation on its respective service route using `http-swagger` ONLY when `Debug` is true. 
- DONT create or define api with PUT method.
