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

```mermaid
flowchart TD
    subgraph Triggers["🚀 Triggers"]
        PushMain["Push to Main"]
        PushRelease["Push to release/*"]
        PR["Pull Request"]
    end

    subgraph Build["📦 Build Stage"]
        Checkout["Checkout"]
        Install["Install Deps"]
        Lint["Lint & Type Check"]
        Test["Run Tests"]
        Docker["Build Docker Image"]
        Scan["Security Scan"]
    end

    subgraph Push["📤 Push Stage"]
        Tag["Tag Image"]
        PushACR["Push to ACR"]
    end

    subgraph Deploy["🚀 Deploy Stage"]
        Update["Update ACA"]
        Health["Health Check"]
        Verify["Verify"]
    end

    subgraph Release["🏷️ Release Stage"]
        ReleaseNotes["Create Release"]
        TagGit["Git Tag"]
    end

    Triggers --> Build
    Build --> Push
    Push --> Deploy
    Deploy -->|Success| Release
    Deploy -->|Fail| Alert["Alert & Rollback"]

    classDef trigger fill:#d83b01,stroke:#fff,stroke-width:2px,color:#fff
    classDef stage fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef decision fill:#5c2d91,stroke:#ffff00,stroke-width:2px,color:#fff

    class Triggers trigger
    class Build,Push,Deploy,Release stage
    class Alert decision
```

## Pipeline Triggers

| Event | Branch | Action |
|-------|--------|--------|
| Push | main | Full deploy |
| Push | release/* | Stage deploy |
| Pull Request | any | Build only |
| Tag | v*.*.* | Release deploy |

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
