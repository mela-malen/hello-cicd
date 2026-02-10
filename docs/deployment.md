---
layout: default
title: Deployment
nav_order: 4
has_children: true
---

<div class="neon-page-header">
  <h1 class="neon-heading">☁️ DEPLOYMENT</h1>
</div>

## Azure Deployment

Complete guide to deploying on Azure Container Apps with CI/CD.

## Contents

| Page | Description |
|------|-------------|
| [Azure Deployment](deployment/azure.md) | Azure setup and deployment |
| [CI/CD Pipeline](deployment/cicd.md) | GitHub Actions workflow |
| [Monitoring](deployment/monitoring.md) | Azure monitoring setup |

## Architecture

```
GitHub → GitHub Actions → Azure Container Registry → Azure Container Apps
                                                    ↓
                                            Health Checks
```

## Quick Links

- [← Back to Home](README.md)
- [Development →](development/setup.md)
- [Guides →](guides/contributing.md)

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
