---
layout: default
title: Diagrams
nav_order: 99
---

<div class="neon-page-header">
  <h1 class="neon-heading">📊 DIAGRAMS</h1>
</div>

## System Architecture

```mermaid
graph TB
    subgraph Users["Users & Clients"]
        Browser[Web Browser]
        Mobile[Mobile App]
        API[API Client]
    end

    subgraph Azure["Azure Cloud Infrastructure"]
        subgraph Network["Network Layer"]
            FrontDoor["Azure Front Door"]
            WAF["Web Application Firewall"]
        end

        subgraph Compute["Compute Layer"]
            ACA["Azure Container Apps"]
            subgraph Pods["Container Pods"]
                Pod1["Pod 1 - Flask"]
                Pod2["Pod 2 - Flask"]
                PodN["Pod N - Flask"]
            end
        end

        subgraph Storage["Storage Layer"]
            ACR["Azure Container Registry"]
            KeyVault["Azure Key Vault"]
            SQL["Azure SQL Database"]
        end

        subgraph Monitoring["Observability"]
            LogAnalytics["Log Analytics"]
            Monitor["Azure Monitor"]
        end
    end

    subgraph CI["CI/CD Pipeline"]
        GitHub["GitHub Repository"]
        GHActions["GitHub Actions"]
        GHCR["GitHub Container Registry"]
    end

    %% User connections
    Browser -->|HTTPS| FrontDoor
    Mobile -->|HTTPS| FrontDoor
    API -->|HTTPS| FrontDoor

    %% Network layer
    FrontDoor --> WAF
    WAF --> ACA

    %% Compute layer
    ACA --> Pod1
    ACA --> Pod2
    ACA --> PodN

    %% Storage connections
    Pods -->|Docker Images| ACR
    Pods -->|Secrets| KeyVault
    Pods -->|TCP 1433| SQL

    %% Monitoring
    Pods -->|Logs/Metrics| LogAnalytics
    LogAnalytics --> Monitor

    %% CI/CD connections
    GitHub -->|Push| GHActions
    GHActions -->|Build| GHCR
    GHActions -->|Push Image| ACR
    GHActions -->|Deploy| ACA

    %% Styling
    classDef azure fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff
    classDef compute fill:#00bcf2,stroke:#fff,stroke-width:2px,color:#000
    classDef storage fill:#107c10,stroke:#fff,stroke-width:2px,color:#fff
    classDef pipeline fill:#5c2d91,stroke:#fff,stroke-width:2px,color:#fff
    classDef users fill:#d83b01,stroke:#fff,stroke-width:2px,color:#fff

    class FrontDoor,WAF,KeyVault,SQL,Monitor azure
    class ACA,Pods,Pod1,Pod2,PodN compute
    class ACR,LogAnalytics storage
    class GitHub,GHActions,GHCR pipeline
    class Browser,Mobile,API users
```

---

## CI/CD Pipeline Flow

```mermaid
flowchart TD
    START[Start: Developer Push] --> Checkout[Checkout Code]

    subgraph Build["Build Stage"]
        Checkout --> Install[Install Dependencies]
        Install --> Lint[Run Linters]
        Lint --> Test[Run Tests]
        Test --> BuildDocker[Build Docker Image]
        BuildDocker --> Scan[Security Scan]
    end

    subgraph Push["Push Stage"]
        Scan --> Tag[Tag Image]
        Tag --> PushACR[Push to ACR]
    end

    subgraph Deploy["Deploy Stage"]
        PushACR --> UpdateACA[Update Container App]
        UpdateACA --> HealthCheck[Health Check]
        HealthCheck --> Verify[Verification]
    end

    subgraph Notify["Notification Stage"]
        Verify --> Result{Success?}
        Result -->|Yes| TagRelease[Create GitHub Release]
        Result -->|No| Rollback[Rollback Previous Version]
        TagRelease --> Slack[Notify via Slack]
        Rollback --> Alert[Send Alert]
        Slack --> END[End]
        Alert --> END
    end

    %% Styling
    classDef stages fill:#1a1a2e,stroke:#ff00ff,stroke-width:2px,color:#fff
    classDef decision fill:#2d2d44,stroke:#ffff00,stroke-width:2px,color:#fff
    classDef startend fill:#0a3d62,stroke:#00ff00,stroke-width:2px,color:#fff

    class Build,Push,Deploy,Notify stages
    class Result decision
    class START,END startend
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
    participant DB as Azure SQL
    participant KV as Key Vault

    Dev->>GH: Push to main branch
    GH->>GHA: Trigger workflow
    GHA->>GHA: Checkout code
    GHA->>GHA: Install Python dependencies
    GHA->>GHA: Run tests

    par Build Docker Image
        GHA->>GHA: Build Docker image
        GHA->>GHA: Security scan
    and Push to Registry
        GHA->>ACR: Login with SP
        ACR-->>GHA: Auth token
        GHA->>ACR: Push image with SHA tag
    end

    ACR->>ACA: Image available
    ACA->>ACA: Pull new image
    ACA->>ACA: Create new revision
    ACA->>ACA: Health check (HTTP /health)
    
    alt Health Check Passed
        ACA->>ACA: Route traffic to new revision
        ACA->>Dev: Deployment successful
    else Health Check Failed
        ACA->>ACA: Rollback to previous revision
        ACA->>Dev: Deployment failed - notification sent
    end

    Note over ACA,DB: Secure connection via Private Endpoint
    ACA->>KV: Fetch secrets (connection string)
    KV-->>ACA: Decrypted secrets
    ACA->>DB: Database operations
```

---

## Application Component Architecture

```mermaid
graph TB
    subgraph Presentation["Presentation Layer"]
        subgraph Routes["Flask Blueprints"]
            PublicBP["Public Blueprint"]
            AdminBP["Admin Blueprint"]
            APIBP["API Blueprint"]
        end
        
        subgraph Views["Views/Templates"]
            Home["Home View"]
            Subscribe["Subscribe View"]
            Admin["Admin Dashboard"]
        end
    end

    subgraph Business["Business Logic Layer"]
        subgraph Services["Domain Services"]
            SubService["SubscriptionService"]
            UserService["UserService"]
            NewsletterService["NewsletterService"]
        end
        
        subgraph Validation["Validators"]
            EmailValidator["Email Validator"]
            FormValidator["Form Validator"]
        end
    end

    subgraph Data["Data Layer"]
        subgraph Repositories["Repositories"]
            SubRepo["SubscriberRepository"]
            UserRepo["UserRepository"]
            NewsRepo["NewsletterRepository"]
        end
        
        subgraph ORM["ORM Layer"]
            SQLAlchemy["Flask-SQLAlchemy"]
            Models["SQLAlchemy Models"]
        end
    end

    subgraph External["External Services"]
        Azure["Azure Services"]
        Email["Email Service"]
    end

    %% Connections
    Routes --> Views
    Routes --> Services
    Services --> Repositories
    Repositories --> ORM
    Services --> Validation
    Services --> External

    %% Styling
    classDef layer fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef component fill:#16213e,stroke:#ff00ff,stroke-width:1px,color:#fff
    classDef service fill:#0f3460,stroke:#00ff00,stroke-width:1px,color:#fff

    class Presentation,Business,Data,External layer
    class Routes,Views,Services,Repositories,ORM component
    class SubService,UserService,NewsletterService,EmailValidator service
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

    %% Styling
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

## Scalability & Load Balancing

```mermaid
flowchart TB
    subgraph Users["Traffic Sources"]
        LB["Load Balancer"]
        CD["CDN Edges"]
    end

    subgraph ACA["Azure Container Apps"]
        subgraph Ingress["Ingress Controller"]
            LB["Load Balancer"]
        end
        
        subgraph Instances["Replicas"]
            Replica1["Replica 1\n512MB RAM\n0.5 CPU"]
            Replica2["Replica 2\n512MB RAM\n0.5 CPU"]
            Replica3["Replica N\n512MB RAM\n0.5 CPU"]
        end
    end

    subgraph Scaling["Auto-Scaling"]
        Metrics["KEDA Metrics"]
        Rules["Scaling Rules"]
    end

    Users --> LB
    LB --> Replica1
    LB --> Replica2
    LB --> Replica3

    Replica1 -->|CPU > 70%| Metrics
    Replica2 -->|CPU > 70%| Metrics
    Replica3 -->|CPU > 70%| Metrics
    
    Metrics --> Rules
    Rules -->|Scale Out| Replica3

    %% Styling
    classDef azure fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff
    classDef compute fill:#00bcf2,stroke:#fff,stroke-width:2px,color:#000
    classDef scaling fill:#5c2d91,stroke:#fff,stroke-width:2px,color:#fff

    class LB,CD azure
    class ACA,Ingress,Instances,Replica1,Replica2,Replica3 compute
    class Metrics,Rules scaling
```

---

## Security Architecture

```mermaid
flowchart TB
    subgraph Perimeter["Network Security"]
        WAF["Azure WAF\nOWASP Rules"]
        DDoS["DDoS Protection"]
        TLS["TLS 1.3 Termination"]
    end

    subgraph Application["Application Security"]
        Auth["Azure AD Auth"]
        RBAC["Role-Based Access"]
        Rate["Rate Limiting"]
    end

    subgraph Data["Data Security"]
        Encryption["At-Rest Encryption"]
        TLSData["TLS 1.3 in Transit"]
        Masking["PII Masking"]
    end

    subgraph Identity["Identity & Access"]
        SP["Service Principals"]
        MI["Managed Identity"]
        Secrets["Key Vault"]
    end

    %% Connections
    User -->|HTTPS| Perimeter
    Perimeter --> Application
    Application --> Data
    Application -->|Secrets| Identity

    %% Styling
    classDef security fill:#1a1a2e,stroke:#ff0000,stroke-width:2px,color:#fff
    classDef component fill:#2d2d44,stroke:#ff9900,stroke-width:1px,color:#fff

    class Perimeter,Application,Data,Identity security
    class WAF,DDoS,TLS,Auth,RBAC,Rate,Encryption,TLSData,Masking,SP,MI,Secrets component
```

---

## Development Workflow

```mermaid
flowchart TD
    subgraph Local["Local Development"]
        Code[Write Code] --> TestLocal[Local Tests]
        TestLocal --> Commit[Git Commit]
        Commit --> Push[Git Push]
    end

    subgraph GitHub["GitHub"]
        Push --> PR[Create Pull Request]
        PR --> CI[CI Pipeline]
        CI --> Review[Code Review]
        Review -->|Approved| Merge[Merge to Main]
        Review -->|Changes| Code
    end

    subgraph Deploy["Deployment"]
        Merge --> Trigger[Trigger CD]
        Trigger --> Build[Build & Push]
        Build --> DeployACA[Deploy to ACA]
        DeployACA --> Verify[Verify Deployment]
    end

    %% Styling
    classDef workflow fill:#1a1a2e,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef action fill:#0f3460,stroke:#ff00ff,stroke-width:1px,color:#fff
    classDef gate fill:#5c2d91,stroke:#ffff00,stroke-width:2px,color:#fff

    class Local,GitHub,Deploy workflow
    class Code,TestLocal,Commit,Push,PR,CI,Build,DeployACA,Verify action
    class Review,Merge,Trigger gate
```

---

## Project Structure

```mermaid
graph TD
    root["hello-cicd/"]
    
    root --> README["README.md"]
    root --> Docker["Dockerfile"]
    root --> dockerignore[".dockerignore"]
    root --> reqs["requirements.txt"]
    root --> wsgi["wsgi.py"]
    root --> gitignore[".gitignore"]
    
    root --> app["app/"]
    app --> init["__init__.py"]
    app --> routes["routes/"]
    routes --> public["public.py"]
    routes --> admin["admin.py"]
    routes --> api["api.py"]
    app --> models["models.py"]
    app --> services["services/"]
    services --> subscription["subscription_service.py"]
    services --> user["user_service.py"]
    
    root --> docs["docs/"]
    docs --> overview["overview.md"]
    docs --> architecture["architecture/"]
    architecture --> arch_overview["overview.md"]
    architecture --> api["api.md"]
    architecture --> data_models["data-models.md"]
    docs --> deployment["deployment/"]
    deployment --> azure["azure.md"]
    deployment --> cicd["cicd.md"]
    deployment --> monitoring["monitoring.md"]
    docs --> development["development/"]
    development --> setup["setup.md"]
    development --> workflow["workflow.md"]
    development --> testing["testing.md"]
    docs --> guides["guides/"]
    guides --> contributing["contributing.md"]
    guides --> docker["docker.md"]
    guides --> troubleshooting["troubleshooting.md"]
    docs --> diagrams["diagrams.md"]
    
    root --> github[".github/"]
    github --> workflows["workflows/"]
    workflows --> deploy["deploy.yml"]
    
    root --> scripts["scripts/"]
    
    %% Styling
    classDef folder fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff
    classDef file fill:#1a1a2e,stroke:#00ff00,stroke-width:1px,color:#fff
    classDef root fill:#5c2d91,stroke:#fff,stroke-width:3px,color:#fff

    class root folder
    class docs,app,github,scripts,architecture,deployment,development,guides,workflows,models,routes,services,files folder
    class README,Docker,dockerignore,reqs,wsgi,gitignore,init,public,admin,api,overview,api,data_models,azure,cicd,monitoring,setup,workflow,testing,contributing,docker,troubleshooting,diagrams,deploy,subscription,user file
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
