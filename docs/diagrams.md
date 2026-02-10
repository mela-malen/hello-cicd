---
layout: default
title: Diagrams
nav_order: 99
---

<div class="neon-page-header">
  <h1 class="neon-heading">📊 DIAGRAMS</h1>
</div>

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    User[User] -->|HTTPS| AzureFrontDoor[Azure Front Door]
    AzureFrontDoor -->|Route| ACAA[Azure Container Apps]
    ACAA -->|Scale| Pod1[Pod 1]
    ACAA -->|Scale| Pod2[Pod 2]
    ACAA -->|Scale| PodN[Pod N]
    GitHub[GitHub Actions] -->|Push| ACR[Azure Container Registry]
    ACR -->|Deploy| ACAA
```

## CI/CD Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant GHA as GitHub Actions
    participant ACR as Azure Container Registry
    participant ACA as Azure Container Apps

    Dev->>GH: Push to main
    GH->>GHA: Trigger workflow
    GHA->>GHA: Build Docker image
    GHA->>ACR: Push image
    ACR->>ACA: Deploy update
    ACA->>Dev: Health check passed
```

## Project Structure

```
hello-cicd/
├── README.md              ← Entry Point
├── docs/
│   ├── overview.md       ← Project Overview
│   ├── architecture.md    ← Architecture Index
│   │   ├── overview.md   ← System Architecture
│   │   ├── api.md        ← API Reference
│   │   └── data-models.md← Data Models
│   ├── development.md    ← Development Index
│   │   ├── setup.md      ← Platform Setup
│   │   ├── workflow.md   ← Dev Workflow
│   │   ├── testing.md    ← Testing Guide
│   │   └── style-guide.md← Code Style
│   ├── deployment.md     ← Deployment Index
│   │   ├── azure.md      ← Azure Deployment
│   │   ├── cicd.md       ← CI/CD Pipeline
│   │   └── monitoring.md ← Monitoring Guide
│   └── guides.md         ← Guides Index
│       ├── contributing.md← Contributing
│       ├── docker.md     ← Docker Guide
│       └── troubleshooting.md← Troubleshooting
```

---

[← Back to Home](README.md)

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
