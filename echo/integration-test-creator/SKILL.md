---
name: integration-test-creator
description: Creates HTTP integration tests for Echo v5 API endpoints in this Go backend (Gozar carpooling platform). Use this skill whenever the user asks to write integration tests, API tests, HTTP-level tests, or end-to-end tests for any controller, route, or endpoint in the project. Also trigger when the user says things like "test the booking endpoint", "add tests for profile API", "write tests for auth routes", or "cover this handler with tests" — even if they don't say the word "integration". This skill knows how to wire up Echo with real or mock repositories, inject JWT tokens, and assert on HTTP status codes and JSON responses.
---

# Context

This project is a Go carpooling REST API using **Echo v5**, **GORM + PostgreSQL**, and **Cobra** (module name: `api`).
Read `CLAUDE.md` for the full architecture picture before writing any test.

---

# Integration Test Standards

## File Layout

| What is being tested | Test file path |
|---|---|
| Client-side controller | `internal/service/client/{feature}/integration_test.go` |
| Admin-side controller | `internal/service/admin/{feature}/integration_test.go` |

- Package declaration: **`package <feature>_test`** (black-box, same directory as the controller).
- One file per feature package; add new `Test*` functions to the existing file rather than creating a new one.

---

## Required Imports

```go
import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "api/config"
    "api/pkg/auth"

    "github.com/labstack/echo/v5"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)
```

Add feature-specific imports (`api/internal/service/client/<feature>`, mock/repository packages) as needed.

---

## Echo Test Harness

Always bootstrap Echo the same way — do **not** spin up a full server:

```go
func setupEcho() *echo.Echo {
    e := echo.New()
    // Optionally register global middleware (e.g. middlewares.DeviceID())
    return e
}
```

Use `httptest.NewRecorder()` + `httptest.NewRequest()` for every request:

```go
rec  := httptest.NewRecorder()
req  := httptest.NewRequest(http.MethodPost, "/client/auth/otp/verify", body)
req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
c    := e.NewContext(req, rec)

err  := ctrl.HandlerFunc(c)
require.NoError(t, err)
assert.Equal(t, http.StatusOK, rec.Code)
```

---

## JWT Injection (Authenticated Endpoints)

Never call the real OTP flow. Generate tokens directly with `pkg/auth`:

```go
func makeToken(t *testing.T, userID uint, uid string) string {
    t.Helper()
    // Ensure the JWT secret is initialised for tests
    if config.AppConfig.JWTSecret == "" {
        config.AppConfig.JWTSecret = "test-secret"
    }
    token, err := auth.CreateToken(userID, uid, "", false)
    require.NoError(t, err)
    return token
}
```

Inject into the Echo context **after** `NewContext`:

```go
c.Set("user_id", uint(1))
c.Set("user_uid", "01ABCDEF...")
```

Or supply the `Authorization` header when testing through the full middleware stack:

```go
req.Header.Set("Authorization", "Bearer "+makeToken(t, 1, "01ABCDEF..."))
```

---

## Repository Mocking Strategy

Integration tests target the **HTTP layer** (controller → usecase → mock repository).
Use lightweight hand-written mocks that implement the repository interface, or
use `github.com/stretchr/testify/mock` stubs.

### Hand-written mock pattern

```go
type mockBookingUsecase struct {
    client.BookingUsecase // embed to satisfy the interface
    listFn func(ctx context.Context, ...) ([]models.Booking, int64, error)
}

func (m *mockBookingUsecase) ListDriverBookings(ctx context.Context, driverID uint, page, limit int, status string) ([]models.Booking, int64, error) {
    return m.listFn(ctx, driverID, page, limit, status)
}
```

Wire into the controller under test:

```go
ctrl := NewController(&mockBookingUsecase{...}, request.NewValidator())
```

---

## Error Response Assertions

All error responses follow `request.ErrorResponse`:

```go
type ErrorResponse struct {
    Code    int      `json:"code"`
    Message string   `json:"message"`
    Error   []string `json:"error,omitempty"`
}
```

HTTP status codes and numeric codes come from `config/errors.json`. Key codes:

| Code | HTTP | Meaning |
|------|------|---------|
| 1001 | 400  | Invalid OTP |
| 1002 | 400  | Invalid phone number |
| 1004 | 400  | Invalid input data |
| 2001 | 401  | Unauthorized |
| 2002 | 403  | Forbidden / inactive user |
| 3001 | 404  | Trip not found |
| 3002 | 404  | Booking not found |
| 3003 | 400  | Trip capacity full |
| 3004 | 400  | Already booked |
| 3005 | 400  | Operation not allowed |
| 3007 | 403  | Cannot book own trip |
| 5001 | 401  | Invalid admin credentials |
| 9999 | 500  | Internal server error |

Assert error body:

```go
var errResp request.ErrorResponse
require.NoError(t, json.NewDecoder(rec.Body).Decode(&errResp))
assert.Equal(t, 2001, errResp.Code)
```

---

## Test Structure (Subtests)

Always use `t.Run` subtests for clarity and isolation:

```go
func TestListBookings(t *testing.T) {
    t.Run("returns 200 with paginated bookings", func(t *testing.T) { ... })
    t.Run("returns 401 when not authenticated", func(t *testing.T) { ... })
    t.Run("returns empty list when no bookings exist", func(t *testing.T) { ... })
}
```

---

## Coverage Checklist per Endpoint

For every handler write at minimum:

1. **Happy path** — correct input, authenticated, expected status + response shape.
2. **Unauthenticated** — missing/invalid `Authorization` header → 401.
3. **Invalid input** — malformed JSON or missing required fields → 400.
4. **Not found** — resource does not exist → 404 (where applicable).
5. **Forbidden** — authenticated but wrong owner → 401 or 403.

---

## Workflow

1. Read the controller file (`internal/service/{client|admin}/{feature}/controller.go`) and its routes file.
2. Identify all handler functions and their route registrations.
3. Create or update `integration_test.go` in the same package directory.
4. Define mock usecase(s) covering only the methods exercised by each test.
5. Write `Test*` functions using the harness above.
6. Run `go test ./internal/service/...` and confirm all tests pass.
7. Run `go test ./...` to ensure nothing else was broken.

---

## Constraints & Rules

- **No real DB, no real Redis, no real external HTTP calls** — mock everything below the controller layer.
- **No PUT method** — the project API never uses PUT; don't generate test helpers for it.
- **UID over ID** — all route params and response fields use `UID` (ULID string).
- **`errors.json` must be loadable** — `ResponseWithCode` reads `config/errors.json` at runtime. In tests, either set `CWD` to the project root or pre-load the file. The simplest approach: run tests from the module root (`go test ./...`).
- **No `AutoMigrate` in integration tests** — integration tests mock the repository layer; SQLite + AutoMigrate is reserved for model unit tests in `pkg/testutils`.
- **Module name is `api`** — all internal imports must start with `api/internal/...` or `api/pkg/...`.