---
layout: default
title: Diagrams
nav_order: 99
---

<div class="neon-page-header">
  <h1 class="neon-heading">DIAGRAMS</h1>
</div>

## System Architecture

```mermaid
flowchart TB
    subgraph Users["Users"]
        Browser["Web Browser"]
        Mobile["Mobile Device"]
    end

    subgraph Azure["Azure Cloud - Sweden Central"]
        subgraph Network["Network"]
            CustomDomain["Custom Domain\ndeploj.se"]
        end

        subgraph Compute["Compute"]
            ACA["Azure Container Apps\nca-hello-cicd"]
            subgraph Pods["Container Pod"]
                Container["hello-cicd\nContainer"]
            end
        end

        subgraph Registry["Container Registry"]
            ACR["Azure Container Registry\nacrhellocicda593ac50"]
            Images["Docker Images"]
        end

        subgraph Data["Data"]
            SQL["Azure SQL Database\ndeplojdb1\nGP_S_Gen5"]
        end

        subgraph Observability["Observability"]
            LogAnalytics["Log Analytics\nworkspace-rghellocicd"]
        end
    end

    subgraph CI["CI/CD"]
        GitHub["GitHub Repository\nmela-malen/hello-cicd"]
        Actions["GitHub Actions\nBuild and Deploy"]
    end

    Users -->|HTTPS| CustomDomain
    CustomDomain --> ACA
    ACA --> Pods
    Pods --> Images
    Pods --> SQL
    Pods --> LogAnalytics
    GitHub -->|Push| Actions
    Actions -->|Build & Push| ACR
    ACR -->|Deploy| ACA

    classDef azure fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff
    classDef compute fill:#00bcf2,stroke:#fff,stroke-width:2px,color:#000
    classDef storage fill:#107c10,stroke:#fff,stroke-width:2px,color:#fff
    classDef pipeline fill:#5c2d91,stroke:#fff,stroke-width:2px,color:#fff
    classDef users fill:#d83b01,stroke:#fff,stroke-width:2px,color:#fff

    class Azure,Network,Compute,Data,Observability azure
    class ACA,Pods,Container compute
    class ACR,Images,SQL storage
    class GitHub,Actions pipeline
    class Users,Browser,Mobile users
```

---

## CI/CD Pipeline Flow

```mermaid
flowchart TD
    subgraph Triggers["Triggers"]
        PushMain["Push to main"]
        PR["PR to main"]
    end

    subgraph Test["Job: test"]
        CheckoutT["Checkout"]
        Python["Setup Python 3.11"]
        Install["Install deps + Playwright"]
        UnitTest["Run unit tests"]
        E2ETest["Run E2E tests"]
    end

    subgraph Build["Job: build-and-deploy"]
        CheckoutB["Checkout"]
        AzureLogin["Azure Login\nOIDC with MI"]
        BuildACR["Build & Push to ACR\naz acr build"]
        DeployACA["Deploy to Container App\naz containerapp update"]
        HealthCheck["Health check\ncurl FQDN 5x"]
    end

    subgraph Result["Result"]
        Success["Deploy successful"]
        Fail["Deploy failed"]
    end

    Triggers --> Test
    Test -->|pass| Build
    Test -->|fail| Fail
    Build -->|pass| HealthCheck
    HealthCheck -->|pass| Success
    HealthCheck -->|fail| Fail

    classDef trigger fill:#d83b01,stroke:#fff,stroke-width:2px,color:#fff
    classDef job fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef result fill:#107c10,stroke:#fff,stroke-width:2px,color:#fff

    class Triggers,PushMain,PR trigger
    class Test,Build,CheckoutT,Python,Install,UnitTest,E2ETest,CheckoutB,AzureLogin,BuildACR,DeployACA,HealthCheck job
    class Success,Fail result
```

---

## Deployment Sequence

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant GHA as GitHub Actions
    participant ACR as Azure Container Registry
    participant ACA as Azure Container Apps
    participant DB as Azure SQL Database

    Dev->>GH: Push to main
    GH->>GHA: Trigger workflow

    Note over GHA: Job: test
    GHA->>GHA: Checkout code
    GHA->>GHA: Setup Python 3.11
    GHA->>GHA: Install dependencies
    GHA->>GHA: Run unit tests
    GHA->>GHA: Run E2E tests

    GHA->>GHA: Job: build-and-deploy
    GHA->>GHA: Checkout code
    GHA->>ACR: az acr build (login via OIDC)
    ACR-->>GHA: Image pushed

    ACA->>ACA: Pull new image
    ACA->>ACA: Update revision

    par Health Check
        ACA->>ACA: Health check /health
    and Update Env Vars
        ACA->>ACA: DB_SERVER, DB_NAME, etc.
    end

    alt Health check passed
        ACA->>ACA: Route traffic to new revision
        ACA->>Dev: Deployment successful
    else Health check failed
        ACA->>ACA: Rollback
        ACA->>Dev: Deployment failed
    end

    ACA->>DB: SQL connections
```

---

## Application Component Architecture

```mermaid
flowchart TB
    subgraph Presentation["Presentation Layer"]
        subgraph Blueprints["Flask Blueprints"]
            PublicBP["Public Blueprint\n/"]
            AdminBP["Admin Blueprint\n/admin"]
        end

        subgraph Views["Views"]
            Home["Home View"]
            Subscribe["Subscribe View"]
            Admin["Admin Dashboard"]
        end
    end

    subgraph Business["Business Logic Layer"]
        subgraph Services["Services"]
            SubService["SubscriptionService"]
            UserService["UserService"]
        end

        subgraph Validation["Validators"]
            EmailValidator["Email Validator"]
        end
    end

    subgraph Data["Data Layer"]
        subgraph Repositories["Repositories"]
            SubRepo["SubscriberRepository"]
            UserRepo["UserRepository"]
        end

        subgraph ORM["ORM Layer"]
            SQLAlchemy["Flask-SQLAlchemy"]
            Models["SQLAlchemy Models"]
        end
    end

    Blueprints --> Views
    Blueprints --> Services
    Services --> Repositories
    Services --> Validation
    Repositories --> ORM

    classDef layer fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef component fill:#16213e,stroke:#ff00ff,stroke-width:1px,color:#fff

    class Presentation,Business,Data layer
    class Blueprints,Views,Services,Repositories,ORM,PublicBP,AdminBP,Home,Subscribe,Admin,SubService,UserService,EmailValidator,SubRepo,UserRepo component
```

---

## Data Flow: Subscription Process

```mermaid
flowchart TD
    Start([User submits subscription]) --> Form["POST /subscribe/confirm"]

    subgraph Validation["Validation Stage"]
        Form --> Validate1[Check required fields]
        Validate1 --> Validate2[Validate email format]
        Validate2 --> Validate3[Check newsletter selection]
        Validate1 -->|Invalid| Error1[Return errors]
        Error1 --> Form
    end

    subgraph Processing["Processing Stage"]
        Validate3 --> Normalize["Normalize email"]
        Normalize --> CheckDup["Check duplicates"]

        CheckDup -->|Already exists| Update["Update existing"]
        CheckDup -->|New| Create["Create new subscriber"]
    end

    subgraph Storage["Database Stage"]
        Update --> Repo["SubscriberRepository.save()"]
        Create --> Repo
        Repo --> DB[("Azure SQL Database")]
        DB -->|Insert/Update| Result[Database committed]
    end

    subgraph Response["Response Stage"]
        Result --> Render["Render thank_you.html"]
        Render --> Success([Success - Thank you page])
    end

    classDef process fill:#1a1a2e,stroke:#00ff00,stroke-width:2px,color:#fff
    classDef storage fill:#0f3460,stroke:#ffff00,stroke-width:2px,color:#fff
    classDef decision fill:#2d2d44,stroke:#ff9900,stroke-width:2px,color:#fff
    classDef startend fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff

    class Validation,Processing,Storage,Response process
    class DB storage
    class CheckDup decision
    class Start,Success startend
```

---

## Database Schema

```mermaid
erDiagram
    USER ||--o{ SUBSCRIBER : manages
    SUBSCRIBER ||--o{ NEWSLETTER_SUBSCRIPTION : has

    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        datetime created_at
        datetime last_login
        boolean is_active
    }

    SUBSCRIBER {
        int id PK
        string name
        string email UK
        datetime created_at
        datetime updated_at
        boolean is_active
    }

    NEWSLETTER {
        int id PK
        string name
        string description
        string slug UK
        boolean is_active
    }

    NEWSLETTER_SUBSCRIPTION {
        int id PK
        int subscriber_id FK
        int newsletter_id FK
        datetime subscribed_at
        boolean is_active
    }

    SUBSCRIBER }o--|| NEWSLETTER : subscribes_to
```

---

## Infrastructure Resources

```mermaid
flowchart TB
    subgraph RG["Resource Group: rg-hello-cicd"]
        subgraph Compute["Container Apps"]
            CAE["Container Apps Environment\ncae-hello-cicd"]
            CA["Container App\nca-hello-cicd\nCPU: 0.5, Memory: 1Gi\nMinReplicas: null, MaxReplicas: 10"]
        end

        subgraph Registry["Container Registry"]
            ACR["Container Registry\nacrhellocicda593ac50\nacrhellocicda593ac50.azurecr.io"]
        end

        subgraph Data["Data"]
            SQLS["SQL Server\ndeplojdb\ndeplojdb.database.windows.net"]
            SQLDB["SQL Database\ndeplojdb1\nGP_S_Gen5"]
        end

        subgraph Identity["Identity"]
            MI["Managed Identity\nid-hello-cicd-deploy\nClientID: d0d0a844-..."]
        end

        subgraph Monitoring["Monitoring"]
            LA["Log Analytics\nworkspace-rghellocicd"]
        end
    end

    subgraph DNS["DNS"]
        Custom["Custom Domain\ndeploj.se\n-> ca-hello-cicd.calmsky-...azurecontainerapps.io"]
    end

    CAE --> CA
    CA --> ACR
    CA --> SQLDB
    CA --> LA
    Custom --> CA

    classDef rg fill:#0078d4,stroke:#fff,stroke-width:3px,color:#fff
    classDef resource fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff

    class RG,Compute,Registry,Data,Identity,Monitoring,DNS rg
    class CAE,CA,ACR,SQLS,SQLDB,MI,LA,Custom resource
```

---

## Security Architecture

```mermaid
flowchart TB
    subgraph Perimeter["Network Security"]
        TLS["TLS/HTTPS"]
    end

    subgraph Application["Application Security"]
        Auth["Azure AD Auth"]
        RBAC["RBAC - Managed Identity"]
        SQLAuth["SQL Authentication"]
    end

    subgraph Data["Data Security"]
        Encryption["Encryption at Rest"]
        TLSData["TLS in Transit"]
    end

    subgraph Identity["Identity & Access"]
        MI["Managed Identity\nid-hello-cicd-deploy"]
        OIDC["OIDC Token"]
    end

    User -->|HTTPS| Perimeter
    Perimeter --> Application
    Application --> Data
    Application -->|OIDC| Identity

    classDef security fill:#1a1a2e,stroke:#ff0000,stroke-width:2px,color:#fff
    classDef component fill:#2d2d44,stroke:#ff9900,stroke-width:1px,color:#fff

    class Perimeter,Application,Data,Identity security
    class TLS,Auth,RBAC,SQLAuth,Encryption,TLSData,MI,OIDC component
```

---

## Project Structure

```mermaid
flowchart TD
    root["hello-cicd/"]

    root --> README["README.md"]
    root --> Docker["Dockerfile"]
    root --> dockerignore[".dockerignore"]
    root --> reqs["requirements.txt"]
    root --> wsgi["wsgi.py"]
    root --> pytest["pytest.ini"]
    root --> gitignore[".gitignore"]

    root --> app["app/"]
    app --> init["__init__.py"]
    app --> routes["routes/"]
    routes --> public["public.py"]
    routes --> admin["admin.py"]
    app --> models["models.py"]
    app --> services["services/"]
    services --> sub["subscription_service.py"]
    services --> user["user_service.py"]
    app --> config["config.py"]

    root --> tests["tests/"]
    tests --> unit["unit/"]
    unit --> test_regression["test_regression.py"]
    unit --> test_sub_repo["test_subscriber_repository.py"]
    unit --> test_sub_svc["test_subscription_service.py"]
    tests --> integration["integration/"]
    integration --> test_routes["test_routes.py"]
    tests --> e2e["e2e/"]
    e2e --> test_visitor["test_visitor_journey.py"]
    e2e --> test_admin["test_admin_journey.py"]

    root --> github[".github/"]
    github --> workflows["workflows/"]
    workflows --> deploy["deploy.yml"]

    root --> docs["docs/"]
    docs --> overview["overview.md"]
    docs --> diagrams["diagrams.md"]
    docs --> visitor["visitor-journey.md"]
    docs --> architecture["architecture/"]
    docs --> deployment["deployment/"]
    docs --> development["development/"]
    docs --> guides["guides/"]

    classDef folder fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff
    classDef file fill:#1a1a2e,stroke:#00ff00,stroke-width:1px,color:#fff

    class root folder
    class docs,app,github,tests,routes,services,unit,integration,e2e,workflows,architecture,deployment,development,guides folder
    class README,Docker,dockerignore,reqs,wsgi,pytest,gitignore,init,public,admin,models,sub,user,config,test_regression,test_sub_repo,test_sub_svc,test_routes,test_visitor,test_admin,deploy,overview,diagrams,visitor file
```

---

[Back to Home](README.md)

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
  text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
  margin: 0;
}
</style>
