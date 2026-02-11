---
layout: default
title: Architecture Overview
nav_order: 1
parent: Architecture
---

<div class="neon-page-header">
  <h1 class="neon-heading">🏗️ SYSTEM ARCHITECTURE</h1>
</div>

## High-Level Overview

```mermaid
graph TD
    subgraph Users["🌍 Users & Traffic"]
        Browser["Web Browser"]
        Mobile["Mobile Apps"]
        API["API Clients"]
    end

    subgraph Azure["☁️ Azure Cloud"]
        subgraph Network["🛡️ Network Layer"]
            FrontDoor["Azure Front Door"]
            WAF["WAF / DDoS Protection"]
        end

        subgraph Compute["⚙️ Compute Layer"]
            ACA["Azure Container Apps"]
            subgraph Pods["📦 Container Pods"]
                Pod1["Pod 1"]
                Pod2["Pod 2"]
                PodN["Pod N"]
            end
        end

        subgraph Storage["💾 Storage Layer"]
            ACR["Container Registry"]
            SQL["Azure SQL"]
            KeyVault["Key Vault"]
        end

        subgraph Observability["📊 Observability"]
            LogAnalytics["Log Analytics"]
            Monitor["Azure Monitor"]
        end
    end

    subgraph CI["🔄 CI/CD"]
        GitHub["GitHub Actions"]
    end

    Users -->|HTTPS| Network
    Network -->|Route| Compute
    Compute -->|Store| Storage
    Compute -->|Logs| Observability
    CI -->|Deploy| Compute
    CI -->|Images| Storage

    classDef azure fill:#0078d4,stroke:#fff,color:#fff
    classDef compute fill:#00bcf2,stroke:#fff,color:#000
    classDef storage fill:#107c10,stroke:#fff,color:#fff
    classDef network fill:#5c2d91,stroke:#fff,color:#fff
    classDef users fill:#d83b01,stroke:#fff,color:#fff

    class Azure,Network,Compute,Storage,Observability azure
    class ACA,Pods,Pod1,Pod2,PodN compute
    class ACR,SQL,KeyVault storage
    class FrontDoor,WAF network
    class Users,Browser,Mobile,API users
```

---

## Application Architecture

### Clean Architecture Layers

```mermaid
graph TB
    subgraph Presentation["🎨 Presentation Layer"]
        Routes["Routes / Blueprints"]
        Views["Jinja2 Templates"]
        Assets["Static Assets (CSS/JS)"]
    end

    subgraph Business["⚡ Business Logic Layer"]
        Services["Domain Services"]
        UseCases["Use Cases"]
        Rules["Business Rules"]
        Validation["Validation Logic"]
    end

    subgraph Data["💾 Data Layer"]
        Repositories["Repositories"]
        ORM["ORM (SQLAlchemy)"]
        Models["Data Models"]
    end

    Routes --> Views
    Routes --> Services
    Services --> UseCases
    UseCases --> Rules
    Services --> Validation
    Services --> Repositories
    Repositories --> ORM
    ORM --> Models

    classDef layer fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef component fill:#16213e,stroke:#ff00ff,stroke-width:1px,color:#fff

    class Presentation,Business,Data layer
    class Routes,Views,Assets,Services,UseCases,Rules,Validation,Repositories,ORM,Models component
```

---

## Component Diagram

```mermaid
graph TB
    subgraph Flask["Flask Application"]
        subgraph Blueprints["📘 Blueprints"]
            Public["Public Blueprint\n/"]
            Admin["Admin Blueprint\n/admin"]
            API["API Blueprint\n/api"]
        end

        subgraph Views["📄 Views"]
            Home["Home View"]
            Subscribe["Subscribe View"]
            AdminDash["Admin Dashboard"]
        end

        subgraph Services["⚙️ Services"]
            SubService["SubscriptionService"]
            UserService["UserService"]
        end

        subgraph Repos["💾 Repositories"]
            SubRepo["SubscriberRepository"]
            UserRepo["UserRepository"]
        end
    end

    subgraph Database["Database"]
        Users["users table"]
        Subscribers["subscribers table"]
        Newsletters["newsletters table"]
    end

    Blueprints --> Views
    Blueprints --> Services
    Services --> Repos
    Repos -->|SQLAlchemy| Database

    classDef flask fill:#1a1a2e,stroke:#00ff00,stroke-width:2px,color:#fff
    classDef component fill:#0d1b2a,stroke:#00ffff,stroke-width:1px,color:#fff
    classDef db fill:#5c2d91,stroke:#fff,stroke-width:2px,color:#fff

    class Flask flask
    class Blueprints,Views,Services,Repos,Public,Admin,API,Home,Subscribe,AdminDash,SubService,UserService,SubRepo,UserRepo component
    class Database,Users,Subscribers,Newsletters db
```

---

## Data Flow

### 1. Subscription Flow

```
1. User submits form → POST /subscribe/confirm
                      │
                      ▼
2. Request Validation (public.py:20-23)
                      │
                      ▼
3. SubscriptionService.subscribe() (subscription_service.py:20-31)
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   Validation: Email     Normalization:
   Pattern check          lowercase, trim
          │                       │
          └───────────┬───────────┘
                      ▼
4. SubscriberRepository.save() (subscriber_repository.py:14-16)
                      │
                      ▼
5. Render thank_you.html with subscriber data
```

---

## Configuration

### Environment-Based Config

| Environment | Config Class | Debug | Purpose |
|-------------|--------------|-------|---------|
| Development | `DevelopmentConfig` | `True` | Local development |
| Testing | `Config` | `False` | Unit testing |
| Production | `ProductionConfig` | `False` | Live deployment |

### Configuration Properties

```python
@dataclass
class Config:
    SECRET_KEY: str           # Session encryption key
    DEBUG: bool              # Debug mode toggle
    TESTING: bool            # Testing mode toggle
    DATABASE_URL: str        # Database connection
    AZURE_CLIENT_ID: str     # Azure AD client
    AZURE_TENANT_ID: str     # Azure AD tenant
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                             │
├─────────────────────────────────────────────────────────────────┤
│  1. NETWORK                                                    │
│     - Azure Front Door (WAF, DDoS protection)                   │
│     - Private endpoints for ACR                                 │
│     - NSG rules restricting access                              │
├─────────────────────────────────────────────────────────────────┤
│  2. APPLICATION                                                 │
│     - HTTPS enforced everywhere                                 │
│     - CORS configuration                                         │
│     - Rate limiting on public endpoints                         │
├─────────────────────────────────────────────────────────────────┤
│  3. DATA                                                        │
│     - Encrypted at rest (Azure storage)                        │
│     - TLS 1.3 for data in transit                              │
│     - PII masking in logs                                       │
├─────────────────────────────────────────────────────────────────┤
│  4. IDENTITY                                                    │
│     - Azure AD authentication                                   │
│     - RBAC for admin access                                     │
│     - Service principal for CI/CD                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Scalability Design

### Horizontal Scaling

```
                    ┌─────────────────┐
                    │   Load Balancer │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │  Pod 1   │      │  Pod 2   │      │  Pod N   │
    │ Flask    │      │ Flask    │      │ Flask    │
    │ 512MB    │      │ 512MB    │      │ 512MB    │
    └──────────┘      └──────────┘      └──────────┘
```

### Scaling Rules

| Metric | Threshold | Action |
|--------|-----------|--------|
| CPU | >70% | Scale up to max replicas |
| Memory | >80% | Scale up to max replicas |
| Request count | >1000/min | Scale up |
| Queue depth | >100 | Scale workers |

---

## Related Documentation

- [Visitor Journey](../visitor-journey.md) | User experience flow & conversion funnel
- [API Reference](api.md)
- [Data Models](data-models.md)
- [Deployment Guide](../deployment/azure.md)
- [Development Setup](../development/setup.md)

---

[← Overview](overview.md) | [Next: API Reference →](api.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #00ffff33;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
  margin: 0;
}
</style>
