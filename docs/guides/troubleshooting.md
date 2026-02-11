---
layout: default
title: Troubleshooting
nav_order: 3
parent: Guides
---

<div class="neon-page-header">
  <h1 class="neon-heading">🔧 TROUBLESHOOTING</h1>
</div>

## Common Issues

### Python Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Activate venv: `source venv/bin/activate` |
| `pip install fails` | Upgrade pip: `pip install --upgrade pip` |
| Python version error | Use Python 3.11+: `python3.11 --version` |

### Docker Issues

| Issue | Solution |
|-------|----------|
| `Permission denied` | Add user to docker group: `sudo usermod -aG docker $USER` |
| `Port already in use` | Kill process: `lsof -ti :5000 | xargs kill` |
| `Container won't start` | Check logs: `docker logs <container>` |

### ODBC Driver Issues

| Issue | Solution |
|-------|----------|
| `ImportError: libodbc.so.2: cannot open shared object file` | **Resolved**: The app now uses `pymssql` (pure Python) instead of pyodbc. No ODBC driver needed! |
| `pyodbc import fails` | **Note**: The application now uses SQLAlchemy with pymssql driver instead of pyodbc. |

### Database Connection

The application now uses SQLAlchemy with pymssql driver for Azure SQL connections, which is a pure Python implementation and doesn't require external ODBC drivers.

### Azure Issues

| Issue | Solution |
|-------|----------|
| `az login fails` | Run `az logout` then `az login` |
| `Deployment failed` | Check resource quotas in Azure portal |
| `Image not found` | Verify ACR login: `az acr login --name <registry>` |

---

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| E001 | Configuration missing | Check `.env` file |
| E002 | Database connection | Verify connection string |
| E003 | Auth failure | Check Azure credentials |
| E004 | Rate limited | Wait and retry |

---

[← Guides](README.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #2e1a1a 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #ff333333;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #ff3333,
    0 0 20px #ff3333;
  margin: 0;
}
</style>
