# Tests

Shared and cross-cutting tests live here. Component-specific tests may also live next to the code they test (backend, frontend).

## Structure (target)

```text
tests/
├── unit/
├── integration/
├── e2e/
├── ai_evaluation/       # Golden tests for AI extraction & safety
└── README.md
```

## Principles

- Prefer small, focused tests.
- Test failure modes (AI unavailable, n8n down, invalid input, etc.).
- See `docs/TESTING_STRATEGY.md`.
