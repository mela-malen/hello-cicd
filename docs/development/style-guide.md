---
layout: default
title: Code Style Guide
nav_order: 4
parent: Development
---

<div class="neon-page-header">
  <h1 class="neon-heading">🎨 CODE STYLE</h1>
</div>

## Style Tools

| Tool | Purpose |
|------|---------|
| Ruff | Linting |
| Black | Formatting |
| Pyright | Type checking |

## Configuration

```toml
# pyproject.toml
[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "UP"]
```

## Python Standards

- Use type hints
- Use dataclasses for models
- Follow PEP 8
- Max line length: 100

---

[← Testing](testing.md)

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
