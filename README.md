# SecureBank Python Backend

> A progressive 14-week Python backend development project that evolves a banking ledger from an in-memory console application into a production-ready SecureBank REST API.

## 1. Project Overview

SecureBank is a structured Python backend development project designed to build practical backend engineering skills through a progressive, requirement-driven implementation. The project begins with an in-memory banking ledger and incrementally introduces data structures, transaction handling, persistence, FastAPI, layered architecture, database integration, validation, authentication, authorization, automated testing, API documentation, pagination, and production integration.

The project follows the weekly progression defined in `R2021_Sem5_Weekly_Python_Backend.pdf`. Each week introduces a specific backend engineering concept and requires implementation, testing, acceptance verification, and an end-of-week deliverable.

The project is being developed as part of the Semester 5 Python Backend mini-project component of the Training & Placement academic program.

---

## 2. Project Objectives

The primary objectives of this project are to:

* Develop strong Python backend programming fundamentals.
* Apply appropriate data structures to realistic banking operations.
* Implement reliable transaction and account-management logic.
* Understand persistence and repository abstraction.
* Build REST APIs using FastAPI.
* Apply layered backend architecture.
* Work with SQLAlchemy and relational databases.
* Implement validation and structured exception handling.
* Implement secure password authentication and JWT-based authorization.
* Develop automated tests using `pytest`.
* Produce clear API documentation.
* Apply pagination and standardized API responses.
* Understand production-oriented backend integration and deployment concepts.
* Develop the ability to explain implementation decisions during technical evaluation and viva.

---

## 3. Technology Progression

The project intentionally progresses from fundamental Python programming to modern backend development.

| Stage     | Primary Technologies / Concepts                                                    |
| --------- | ---------------------------------------------------------------------------------- |
| Weeks 1–3 | Python, dataclasses, dictionaries, `defaultdict`, `bisect`, `SortedDict`, `timeit` |
| Week 4    | JSON, `dataclasses.asdict()`, `pathlib`, repository abstraction, Pydantic          |
| Week 5    | FastAPI, Uvicorn, Pydantic v2, dependency injection, Swagger                       |
| Week 6    | `APIRouter`, `Depends()`, service layer, repository layer, CRUD APIs               |
| Week 7    | SQLAlchemy 2.0, SQLite, PostgreSQL, sessions, `select()`                           |
| Week 8    | Pydantic validation, field constraints, custom validators, exception handlers      |
| Week 9    | Password hashing and authentication fundamentals                                   |
| Week 10   | JWT authentication, `OAuth2PasswordBearer`, PyJWT                                  |
| Week 11   | Role-based authorization and ownership checks                                      |
| Week 12   | `pytest`, HTTP testing, mocking, automated test coverage                           |
| Week 13   | OpenAPI documentation, pagination, standardized responses                          |
| Week 14   | Docker, production ASGI serving, final integration and viva readiness              |

---

## 4. Weekly Development Roadmap

### Week 1 — Account Fundamentals

**Focus:** In-memory account management.

Implemented functionality:

* Create account
* Deposit money
* Withdraw money
* Check balance
* Close account
* Account validation
* Custom exceptions
* CLI-based interaction

Core concepts:

* `dict[int, Account]`
* `@dataclass`
* Dictionary-based O(1) account access
* Custom exceptions
* Input validation

Deliverable:

```text
bank_console.py
```

---

### Week 2 — Transfers, Reversals & Multi-Key Customer Indexing

**Focus:** Transaction operations and secondary indexing.

Implemented functionality:

* Transfer money between accounts
* Atomic transfer behavior
* Manual rollback on failed transfers
* Transaction logging
* Reversal of the latest transaction
* Customer-name secondary index
* Multiple accounts associated with the same customer

Core concepts:

* `dict`
* `collections.defaultdict`
* `@dataclass`
* Transaction history
* Manual rollback using `try/except`
* Conservation of total system balance

Deliverable:

```text
Extended bank_console.py
```

---

### Week 3 — Sorted Statements & Range Queries

**Focus:** Ordered data structures.

Planned functionality:

* Sorted account listings by ID
* Sorted account listings by balance
* Sorted transaction history
* Date-range transaction statements
* `bisect.insort()`
* `bisect_left()`
* `bisect_right()`
* `SortedDict`
* `SortedDict.irange()`
* `timeit` performance benchmarking

Special consideration:

Transaction timestamps require a tie-breaker so that two transactions occurring at the same timestamp are not accidentally overwritten.

Deliverable:

```text
statement_service.py
```

plus a short benchmark report.

---

### Week 4 — JSON Persistence & Repository Bridge

**Focus:** Persistence and abstraction.

Planned functionality:

* Persist accounts to JSON
* Persist transaction history
* Restore data after restart
* Repository abstraction
* JSON repository implementation
* DTO-based data exposure

Core concepts:

* `json`
* `pathlib.Path`
* `ABC`
* `@abstractmethod`
* `dataclasses.asdict()`
* Pydantic models
* `Optional`

Deliverable:

```text
JSON-backed repository + DTO layer
```

---

### Week 5 — FastAPI Foundations

**Focus:** First REST API.

Planned functionality:

* FastAPI application
* `GET /accounts`
* `GET /accounts/{id}`
* Explicit response models
* Dependency injection
* Interactive API documentation

Documentation endpoints:

```text
/docs
/redoc
```

Deliverable:

```text
Runnable FastAPI application
+ exported request collection
```

---

### Week 6 — Layered Architecture

**Focus:** Separation of responsibilities.

Architecture:

```text
Router
   ↓
Service
   ↓
Repository
```

Planned functionality:

* Full CRUD API
* Transfer API
* Reversal API
* Dependency-based service/repository wiring

Core principle:

> Routers handle HTTP concerns; business rules belong in the service layer; persistence belongs in the repository layer.

Deliverable:

```text
Full CRUD API
+ updated request collection
```

---

### Week 7 — SQLAlchemy Persistence

**Focus:** Real database persistence.

Planned functionality:

* SQLAlchemy 2.0-style models
* SQLite development database
* PostgreSQL production-style database
* Session-per-request pattern
* Filtered database queries
* No hand-written SQL strings

Core concepts:

* `Mapped`
* `mapped_column`
* `sessionmaker`
* `select()`
* FastAPI database dependencies

Deliverable:

```text
SQLAlchemy-backed SecureBank API
```

---

### Week 8 — Validation & Exception Handling

**Focus:** Reliable API validation and error handling.

Planned functionality:

* Pydantic field constraints
* Custom validators
* Global exception handlers
* Structured validation errors
* Business exceptions

Expected behavior includes appropriate status codes for:

* Validation failures
* Missing accounts
* Insufficient funds
* Other client-side errors

Deliverable:

```text
Global exception handlers
+ validated Pydantic models
+ negative test suite
```

---

### Week 9 — Authentication Fundamentals

**Focus:** Secure credential handling.

Planned functionality:

* Password hashing
* User authentication fundamentals
* Secure credential storage
* Authentication-related validation

Passwords must never be stored or exposed in plain text.

---

### Week 10 — JWT Authentication

**Focus:** Token-based authentication.

Planned functionality:

* JWT generation
* JWT validation
* `OAuth2PasswordBearer`
* Protected endpoints
* Authentication dependencies

---

### Week 11 — Authorization

**Focus:** Access control.

Planned functionality:

* Role-based authorization
* Ownership checks
* Permission enforcement
* Protected banking operations

The system must distinguish authentication from authorization.

---

### Week 12 — Automated Testing

**Focus:** Production-oriented testing.

Planned functionality:

* Service-layer unit tests
* Repository mocking
* API integration tests
* Authenticated request testing
* Failure-path testing
* Coverage measurement

Primary tools:

```text
pytest
pytest-mock
TestClient / httpx
pytest-asyncio
pytest --cov
```

Target:

```text
15+ automated tests
```

---

### Week 13 — API Documentation & Pagination

**Focus:** Professional API usability.

Planned functionality:

* Improved Swagger documentation
* Response models
* Tags
* Examples
* Pagination
* Standardized response envelope
* OpenAPI export

Target response structure:

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

---

### Week 14 — Production Integration & Viva Readiness

**Focus:** Final integration.

Planned functionality:

* Integrate Weeks 5–13
* Docker
* Docker Compose
* Production ASGI serving
* PostgreSQL integration
* Externalized configuration
* Final end-to-end testing
* Viva preparation

Production serving must not rely on the development-only reload configuration.

Deliverables:

```text
Dockerfile
docker-compose.yml
README
Final integrated SecureBank API
```

---

## 5. Repository Structure

The repository is organized by weekly development milestones.

```text
PYTHON-BACKEND-PROJECT/
│
├── WEEK - 1/
│   ├── README.md
│   ├── account.py
│   ├── bank.py
│   ├── exceptions.py
│   └── main.py
│
├── WEEK - 2/
│   ├── README.md
│   ├── TESTING.md
│   ├── account.py
│   ├── bank.py
│   ├── main.py
│   ├── storage_manager.py
│   ├── transaction.py
│   ├── test_bank.py
│   ├── test_edge_cases.py
│   ├── test_persistence.py
│   └── test_storage.py
│
├── WEEK - 3/
│   ├── statement_service.py
│   ├── test_statement_service.py
│   └── ...
│
├── WEEK - 4/
│   └── ...
│
├── ...
│
├── LICENSE
└── README.md
```

Additional personal or experimental folders may exist in the repository but are outside the scope of the official weekly SecureBank implementation.

---

## 6. Development Principles

The project follows these principles throughout development:

### Correctness

Every weekly feature must satisfy its specified test case and acceptance criteria before being considered complete.

### Incremental Development

Each week builds on concepts introduced earlier rather than replacing working functionality without reason.

### Separation of Responsibilities

As the project evolves, business logic, API handling, persistence, validation, and security responsibilities are kept appropriately separated.

### Defensive Programming

Invalid input, missing accounts, insufficient funds, failed operations, and other expected error conditions must be handled explicitly.

### Test-Driven Verification

Tests are used to prove important invariants and failure paths rather than testing only successful scenarios.

### No Silent Data Corruption

Operations involving balances and transactions must preserve correctness even when an operation fails.

---

## 7. Important Banking Invariants

The following principles are treated as correctness requirements:

### Transfer Conservation

For a successful transfer:

```text
Total balance before transfer
=
Total balance after transfer
```

The transfer changes ownership of funds but does not create or destroy money.

### Atomic Failure

If the destination account is invalid or the transfer cannot complete:

```text
Sender balance before
=
Sender balance after
```

No partial debit is allowed.

### Transaction Integrity

Every successful transaction must be recorded consistently with the account state.

### Account Safety

Operations involving closed or non-existent accounts must be rejected cleanly rather than producing an unhandled exception.

---

## 8. Testing Strategy

Testing is performed at each stage of development.

Typical commands include:

```powershell
python -m pytest -q
```

For detailed test names:

```powershell
python -m pytest -vv
```

For syntax verification:

```powershell
python -m py_compile <file.py>
```

Before committing a change, the relevant tests must pass.

The project prioritizes:

* Happy-path tests
* Invalid-input tests
* Failure-path tests
* Invariant tests
* Regression tests
* Edge-case tests
* API integration tests in later weeks

Because the Training & Placement Planner specifies that the Python backend mini-project assessment and corresponding internal marks are based on test performance, passing and meaningful tests are treated as a core project requirement rather than an optional activity.

---

## 9. Version Control

The repository is maintained using Git and GitHub.

Commits should describe one logical change and use clear Conventional Commit-style messages.

Examples:

```text
feat(week2): add atomic account transfer
test(week2): add transfer rollback tests
fix(week2): prevent partial transfer on invalid target
docs(week2): document transaction reversal workflow
refactor(week3): isolate sorted statement logic
```

Avoid vague commit messages such as:

```text
fix
update
changes
wip
final
```

Each weekly development stage should be committed only after the implementation has been tested successfully.

---

## 10. Quality Gate Before Completion

A weekly implementation is considered complete only after:

* Required functionality is implemented.
* Required data structures and techniques are used.
* Official test cases are satisfied.
* Edge cases are tested.
* Existing functionality continues to work.
* Code has been syntax-checked.
* No avoidable errors remain.
* Documentation accurately describes the implementation.
* Git changes are reviewed before committing.

---

## 11. Current Development Status

The project is being developed progressively according to the weekly Python Backend curriculum.

Completed:

```text
Week 1 — Account Fundamentals
Week 2 — Transfers, Reversals & Customer Indexing
```

In progress:

```text
Week 3 — Sorted Statements & Range Queries
```

Upcoming:

```text
Week 4 — JSON Persistence & Repository Bridge
Week 5 — FastAPI Foundations
Week 6 — Layered Architecture
Week 7 — SQLAlchemy Persistence
Week 8 — Validation & Exception Handling
Week 9 — Authentication Fundamentals
Week 10 — JWT Authentication
Week 11 — Authorization
Week 12 — Automated Testing
Week 13 — API Documentation & Pagination
Week 14 — Production Integration & Viva Readiness
```

---

## 12. Documentation Policy

Documentation is updated whenever a change materially affects:

* Project functionality
* Setup instructions
* Testing commands
* Repository structure
* Development workflow
* Major technical decisions

Documentation must describe the actual implementation and must not claim functionality that has not yet been implemented.

---

## 13. Academic Context

This project forms part of the Semester 5 Python Backend mini-project component under the Training & Placement academic program.

The project follows the dedicated weekly Python Backend development document:

```text
R2021_Sem5_Weekly_Python_Backend.pdf
```

The project is intended to provide structured, progressive backend development practice and is evaluated through the prescribed assessment process.

---

## 14. License

This project is released under the MIT License.

See:

```text
LICENSE
```

for the complete license text.

---

## 15. Author

**Sivanesh K**

Python Backend Development Project

Semester 5 — B.Tech Artificial Intelligence and Data Science

J.J. College of Engineering and Technology

---

## 16. Reference

Primary technical curriculum:

```text
R2021_Sem5_Weekly_Python_Backend.pdf
```

Academic / placement context:

```text
R2021_Sem5_Placement_Planner_V1.2_28Jul2026.docx
```

Repository:

```text
https://github.com/sivaneshk23/PYTHON-BACKEND-PROJECT
```
