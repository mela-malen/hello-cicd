---
layout: default
title: Development Workflow
nav_order: 2
parent: Development
---

<div class="neon-page-header">
  <h1 class="neon-heading">🔄 WORKFLOW</h1>
</div>

## Daily Development

```bash
# 1. Sync with main
git checkout main
git pull upstream main

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes
# ... edit code ...

# 4. Run tests
pytest

# 5. Commit changes
git add .
git commit -m "feat: add new feature"

# 6. Push to fork
git push origin feature/new-feature

# 7. Create PR on GitHub
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_subscription.py
```

---

[← Setup](setup.md) | [Next: Testing →](testing.md)

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
