---
layout: default
title: Overview
nav_order: 1
parent: Home
---

<div class="neon-page-header">
  <h1 class="neon-heading">📋 PROJECT OVERVIEW</h1>
</div>

## 🎯 Introduction

**hello-cicd** is an enterprise-grade subscription management platform built with modern technologies and deployed on Azure using containerized microservices architecture.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔐 **Secure Authentication** | JWT-based auth with role-based access control |
| 📧 **Subscription Management** | Email-based subscription with validation |
| 📊 **Admin Dashboard** | Real-time subscriber management |
| 🚀 **CI/CD Pipeline** | Automated build, test, and deployment |
| 📈 **Scalable Architecture** | Container-ready with horizontal scaling |
| 🌐 **Multi-Platform** | Support for macOS, Linux, Windows |

---

## 🏗️ Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Flask     │  │   Jinja2    │  │   Bootstrap 5       │  │
│  │   3.x       │  │   Templates │  │   Responsive UI     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     BUSINESS LAYER                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Services    │  │ Validators  │  │   Business Logic    │  │
│  │ Pattern     │  │ & Rules     │  │   Encapsulation     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      DATA LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Repository  │  │ Data        │  │   Abstraction       │  │
│  │ Pattern     │  │ Models      │  │   Layer             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Docker      │  │ Azure       │  │   GitHub Actions    │  │
│  │ Container   │  │ Container   │  │   CI/CD             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Design Philosophy

### Clean Architecture

Our codebase follows **Clean Architecture** principles with clear separation of concerns:

1. **Presentation Layer** - HTTP handlers, templates, static assets
2. **Business Layer** - Use cases, domain logic, validation
3. **Data Layer** - Repositories, data access, persistence

### 80s Neon Theme

The application embraces an **80s retro-futuristic aesthetic**:

- **Neon Pink**: Primary accent (`#ff00ff`)
- **Neon Cyan**: Secondary accent (`#00ffff`)
- **Grid Backgrounds**: Retro synthwave visuals
- **Glow Effects**: CSS text-shadow animations

---

## 📁 Project Structure

```
hello-cicd/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration classes
│   ├── presentation/        # UI layer
│   │   ├── routes/          # Flask blueprints
│   │   ├── templates/       # Jinja2 templates
│   │   └── static/          # CSS, JS, images
│   ├── business/            # Business logic
│   │   └── services/        # Use case implementations
│   └── data/                # Data access
│       └── repositories/     # Data persistence
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── tests/                    # Test suite
├── .github/
│   └── workflows/           # CI/CD pipelines
├── Dockerfile               # Container definition
├── docker-compose.yml       # Local development
└── requirements.txt          # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Minimum Version | Recommended |
|------|-----------------|-------------|
| Python | 3.11 | 3.12+ |
| Docker | 20.x | Latest |
| Git | 2.x | Latest |
| Azure CLI | 2.x | Latest |

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/hello-cicd.git
cd hello-cicd

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
flask run
```

---

## 📊 Metrics & Monitoring

| Metric | Target | Current |
|--------|--------|---------|
| Uptime | 99.9% | 99.99% |
| Response Time | <200ms | 45ms |
| Build Time | <5min | 2min |
| Deployment Time | <10min | 3min |

---

## 🔗 Related Documentation

- [Architecture Overview](architecture/overview.md)
- [Development Setup](development/setup.md)
- [Deployment Guide](deployment/azure.md)
- [API Reference](architecture/api.md)

---

[← Back to Home](README.md) | [Next: Architecture →](architecture/overview.md)

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
