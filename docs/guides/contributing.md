---
layout: default
title: Contributing Guide
nav_order: 1
parent: Guides
---

<div class="neon-page-header">
  <h1 class="neon-heading">🤝 CONTRIBUTING</h1>
</div>

## Welcome

Thank you for considering contributing to hello-cicd! This guide outlines the process for contributing to our project.

---

## Getting Started

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Development |
| Git | 2.x | Version control |
| Docker | 20.x+ | Containerization |
| Jira Account | - | Issue tracking |

### Setting Up Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/hello-cicd.git
cd hello-cicd

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/hello-cicd.git

# Create feature branch
git checkout -b feature/amazing-new-feature

# Setup development environment
./scripts/setup.sh  # or scripts/setup.ps1 on Windows
```

---

## Development Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CONTRIBUTION WORKFLOW                               │
│                                                                              │
│  1. Create Issue (Jira) ──────▶ 2. Create Branch ──────▶ 3. Make Changes     │
│         │                            │                       │              │
│         │                            ▼                       ▼              │
│         │                    ┌──────────────┐      ┌──────────────┐        │
│         │                    │  Feature/    │      │  Write Code  │        │
│         │                    │  Bugfix/     │      │  Add Tests   │        │
│         │                    │  Hotfix      │      │  Update Docs │        │
│         │                    └──────────────┘      └──────────────┘        │
│         │                            │                       │              │
│         │                            ▼                       ▼              │
│         │                    4. Push Branch ──────▶ 5. Create PR           │
│         │                                    │              │              │
│         │                                    ▼              ▼              │
│         │                            ┌──────────────┐ ┌──────────────┐      │
│         │                            │  GitHub      │ │ CI/CD       │      │
│         │                            │  PR Review   │ │ Tests Pass  │      │
│         │                            └──────────────┘ └──────────────┘      │
│         │                                    │              │              │
│         └────────────────────────────────────┴──────────────┘              │
│                                   │                                         │
│                                   ▼                                         │
│                          6. Merge to Main                                    │
│                                   │                                         │
│                                   ▼                                         │
│                          7. Deploy to Azure                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Issue Tracking

### Creating Issues

**Use Jira for all issue tracking:**

| Issue Type | Prefix | Description |
|------------|--------|-------------|
| Feature | `FEAT` | New functionality |
| Bug | `BUG` | Something isn't working |
| Task | `TASK` | Maintenance work |
| Epic | `EPIC` | Large feature initiative |

### Issue Templates

```markdown
---
title: "[FEAT] Add new subscription feature"
type: Feature
description: |
  As a [user role],
  I want to [action],
  So that [benefit].
acceptance_criteria:
  - [ ] Criterion 1
  - [ ] Criterion 2
---
```

---

## Branch Naming Convention

| Branch Type | Pattern | Example |
|-------------|---------|---------|
| Feature | `feature/JIRA-XXX-description` | `feature/HELLO-123-add-dashboard` |
| Bugfix | `bugfix/JIRA-XXX-description` | `bugfix/HELLO-456-fix-login` |
| Hotfix | `hotfix/JIRA-XXX-description` | `hotfix/HELLO-789-security-patch` |
| Release | `release/v1.2.0` | `release/v1.2.0` |

---

## Coding Standards

### Python Style

| Tool | Configuration |
|------|---------------|
| Linter | Ruff |
| Formatter | Black |
| Type Checker | Pyright |
| Max Line Length | 100 |

### Code Example

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class Subscriber:
    """Represents a newsletter subscriber."""
    email: str
    name: str
    subscribed_at: Optional[datetime] = None


def subscribe(email: str, name: str) -> SubscriberResult:
    """
    Subscribe a new user to the newsletter.

    Args:
        email: The subscriber's email address
        name: The subscriber's display name

    Returns:
        SubscriptionResult with success status and data
    """
    # Validation logic
    validated_email = _validate_email(email)
    if not validated_email:
        return SubscriptionResult(success=False, error="Invalid email")

    # Create subscriber
    subscriber = Subscriber(email=validated_email, name=name)

    return SubscriptionResult(success=True, subscriber=subscriber)
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance |

### Example

```
feat(subscription): add email validation with regex

Implement email validation using RFC 5322 regex pattern.
Reject invalid email formats before processing subscription.

Closes HELLO-123
```

---

## Pull Request Process

### PR Requirements

| Requirement | Status |
|-------------|--------|
| All CI checks pass | ✅ Required |
| Code reviewed | ✅ Required |
| Tests added/updated | ✅ Required |
| Documentation updated | ✅ Required |
| No merge conflicts | ✅ Required |

### PR Template

```markdown
## Description
Brief description of changes

## Jira Issue
HELLO-XXX

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Tested locally
- [ ] Tested on staging

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] No new warnings
```

---

## Review Process

### Reviewers

| Role | Responsibility |
|------|----------------|
| Core Team | Required approval |
| Security Team | For security changes |
| Docs Team | For documentation changes |

### Review Checklist

- [ ] Code is properly tested
- [ ] No security vulnerabilities
- [ ] Documentation is updated
- [ ] No breaking changes without notice
- [ ] Follows coding standards
- [ ] Commit history is clean

---

## Development Tools

### Recommended Setup

| Tool | Purpose | Platform |
|------|---------|---------|
| VS Code | IDE | All |
| PyCharm | IDE | All |
| Docker Desktop | Container dev | All |
| Azure CLI | Cloud access | All |
| Jira | Issue tracking | Web |
| GitHub | PR management | Web |

### VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-azuretools.vscode-docker",
    "github.vscode-pull-request-github",
    "dbaeumer.vscode-eslint"
  ]
}
```

---

## Related Documentation

- [Development Setup](../development/setup.md)
- [Architecture Overview](../architecture/overview.md)
- [API Reference](../architecture/api.md)
- [Deployment Guide](../deployment/azure.md)

---

[← Guides Home](README.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #2e1a47 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #ffaa0033;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #ffaa00,
    0 0 20px #ffaa00;
  margin: 0;
}
</style>
