---
layout: default
title: Testing Guide
nav_order: 3
parent: Development
---

<div class="neon-page-header">
  <h1 class="neon-heading">🧪 TESTING</h1>
</div>

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_subscription.py

# Run with verbose output
pytest -v
```

## Test Structure

```
tests/
├── unit/
│   ├── test_subscription_service.py
│   └── test_subscriber_repository.py
├── integration/
│   └── test_routes.py
└── conftest.py
```

---

[← Workflow](workflow.md) | [Next: Style Guide →](style-guide.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #1a2e1a 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #00ff0033;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #00ff00,
    0 0 20px #00ff00;
  margin: 0;
}
</style>
