---
layout: default
title: Monitoring
nav_order: 3
parent: Deployment
---

<div class="neon-page-header">
  <h1 class="neon-heading">📈 MONITORING</h1>
</div>

## Azure Monitoring

### Key Metrics

| Metric | Threshold | Action |
|--------|-----------|--------|
| CPU Usage | >70% | Scale up |
| Memory Usage | >80% | Alert |
| Request Latency | >500ms | Investigate |
| Error Rate | >1% | Alert |

### Log Analytics

```bash
# Query application logs
az monitor log-analytics query \
  --workspace hello-cicd-logs \
  --analytics-query "ContainerAppConsoleLogs | where TimeGenerated > ago(1h)"
```

---

[← CI/CD Pipeline](cicd.md)

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
