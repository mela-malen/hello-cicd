---
layout: default
title: CI/CD Pipeline
nav_order: 2
parent: Deployment
---

<div class="neon-page-header">
  <h1 class="neon-heading">🔄 CI/CD PIPELINE</h1>
</div>

## Pipeline Flow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Commit   │──▶│ Build    │──▶│ Test     │──▶│ Push     │──▶│ Deploy   │
│ to Main  │    │ Docker   │    │ Suite    │    │ to ACR   │    │ to ACA   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                          │                 │
                                          ▼                 ▼
                                    ┌──────────┐      ┌──────────┐
                                    │ GitHub   │      │ Health   │
                                    │ Release  │      │ Verify   │
                                    └──────────┘      └──────────┘
```

## Triggers

| Event | Branch | Action |
|-------|--------|--------|
| Push | main | Full deploy |
| Push | release/* | Stage deploy |
| Pull Request | any | Build only |

---

[← Azure Deployment](azure.md) | [Next: Monitoring →](monitoring.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #1a2e47 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #0088ff33;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #0088ff,
    0 0 20px #0088ff;
  margin: 0;
}
</style>
