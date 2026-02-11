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
class Subscriber(db.Model):
    """Represents a newsletter subscriber."""
    id: int                   # Primary key
    email: str                # Unique email address
    name: str                 # Display name
    subscribed_at: datetime  # Subscription timestamp (auto-generated)

    # Newsletter subscriptions (boolean flags)
    nl_kost: bool            # Kost & Näring newsletter
    nl_mindset: bool         # Mindset newsletter
    nl_kunskap: bool         # Kunskap & Forskning newsletter
    nl_veckans_pass: bool    # Veckans Pass newsletter
    nl_jaine: bool           # Träna med Jaine newsletter
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

## Newsletter Options

| Field | Newsletter | Description |
|-------|------------|-------------|
| `nl_kost` | Kost & Näring | Recipes and nutrition tips |
| `nl_mindset` | Mindset | Mental strength and focus |
| `nl_kunskap` | Kunskap & Forskning | Science-based training tips |
| `nl_veckans_pass` | Veckans Pass | Weekly workout routines |
| `nl_jaine` | Träna med Jaine | AI-powered personal training |

---

## Database Schema

```
┌─────────────────┐
│   subscribers   │
├─────────────────┤
│ PK  id          │ INTEGER
│     email       │ VARCHAR(120) UNIQUE
│     name        │ VARCHAR(120)
│     subscribed_at│ DATETIME
│     nl_kost     │ BOOLEAN
│     nl_mindset  │ BOOLEAN
│     nl_kunskap  │ BOOLEAN
│     nl_veckans_pass│ BOOLEAN
│     nl_jaine    │ BOOLEAN
└─────────────────┘
```

---

## Database Connection

The application uses SQLAlchemy ORM with the following configuration:

| Environment | Database | Driver |
|-------------|----------|--------|
| Development | SQLite (in-memory) | sqlite |
| Production | Azure SQL | pymssql (pure Python) |

Connection is configured via environment variables:

| Variable | Description |
|----------|-------------|
| `DB_TYPE` | Database type: `sqlite` or `mssql` |
| `DB_SERVER` | Azure SQL server hostname |
| `DB_NAME` | Database name |
| `DB_USERNAME` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_DRIVER` | Driver: `pymssql` (recommended) or `pyodbc` |

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
