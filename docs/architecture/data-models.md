---
layout: default
title: Data Models
nav_order: 3
parent: Architecture
---

<div class="neon-page-header">
  <h1 class="neon-heading">📊 DATA MODELS</h1>
</div>

## Subscriber

```python
@dataclass
class Subscriber:
    """Represents a newsletter subscriber."""
    email: str              # Primary key, unique identifier
    name: str               # Display name
    subscribed_at: datetime  # Subscription timestamp (auto-generated)
```

## SubscriptionResult

```python
@dataclass
class SubscriptionResult:
    """Result of a subscription operation."""
    success: bool               # Operation success status
    error: str = ""            # Error message if failed
    subscriber: Subscriber | None  # Created subscriber data
```

---

## Database Schema

```
┌─────────────────┐
│   subscribers   │
├─────────────────┤
│ PK  email       │ VARCHAR(255)
│     name        │ VARCHAR(100)
│     subscribed_at│ DATETIME
└─────────────────┘
```

---

[← API Reference](api.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #ff00ff33;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #ff00ff,
    0 0 20px #ff00ff;
  margin: 0;
}
</style>
