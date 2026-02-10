---
layout: default
title: API Reference
nav_order: 2
parent: Architecture
---

<div class="neon-page-header">
  <h1 class="neon-heading">🔌 API REFERENCE</h1>
</div>

## Endpoints Overview

### Public Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/subscribe` | Subscription form |
| POST | `/subscribe/confirm` | Process subscription |

### Admin Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/admin` | Admin dashboard | ✅ Yes |
| GET | `/admin/subscribers` | List subscribers | ✅ Yes |

---

## Public Endpoints

### GET /

Home page - renders the landing page template.

**Response:** `200 OK` - Renders `index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Hello-CICD</title>
</head>
<body>
    <!-- Landing page content -->
</body>
</html>
```

---

### GET /subscribe

Subscription page - displays the email subscription form.

**Response:** `200 OK` - Renders `subscribe.html`

**Template Variables:**

| Variable | Type | Description |
|----------|------|-------------|
| `error` | `str` | Error message (if any) |
| `email` | `str` | Pre-filled email |
| `name` | `str` | Pre-filled name |

---

### POST /subscribe/confiirm

Process a new subscription request.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | `string` | Yes | Subscriber email address |
| `name` | `string` | No | Subscriber name |

**Example Request:**

```bash
curl -X POST https://api.hello-cicd.com/subscribe/confirm \
  -d "email=user@example.com" \
  -d "name=John Doe"
```

**Success Response:** `200 OK` - Renders `thank_you.html`

```json
{
  "success": true,
  "subscriber": {
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Error Response:** `200 OK` - Renders `subscribe.html` with error

```json
{
  "success": false,
  "error": "Invalid email format"
}
```

**Validation Rules:**

| Field | Rule | Error Message |
|-------|------|---------------|
| email | Required | "Email is required" |
| email | Regex match | "Invalid email format" |
| name | Optional | - |

---

## Admin Endpoints

### GET /admin

Admin dashboard overview.

**Requires:** Admin authentication

**Response:** `200 OK` - Renders admin dashboard template

---

### GET /admin/subscribers

List all subscribers.

**Requires:** Admin authentication

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | `int` | 1 | Page number |
| `per_page` | `int` | 50 | Items per page |
| `sort` | `string` | `date` | Sort field |

**Response:** `200 OK`

```json
{
  "subscribers": [
    {
      "email": "user1@example.com",
      "name": "User 1",
      "subscribed_at": "2024-01-15T10:30:00Z"
    },
    {
      "email": "user2@example.com",
      "name": "User 2",
      "subscribed_at": "2024-01-14T15:45:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 150,
    "pages": 3
  }
}
```

---

## Data Models

### Subscriber

```python
@dataclass
class Subscriber:
    email: str          # Primary key
    name: str           # Display name
    subscribed_at: datetime  # Auto-generated
```

### SubscriptionResult

```python
@dataclass
class SubscriptionResult:
    success: bool               # Operation success status
    error: str = ""            # Error message if failed
    subscriber: Subscriber | None  # Created subscriber
```

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "expected": "email format"
    }
  }
}
```

---

## Rate Limiting

| Endpoint | Rate Limit | Window |
|----------|------------|--------|
| `/subscribe/confirm` | 10 req/min | Per IP |
| `/admin/*` | 100 req/min | Per session |

---

[← Architecture Overview](overview.md) | [Next: Data Models →](data-models.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #2e1a47 50%, #0a0a0a 100%);
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
