---
layout: default
title: Home
nav_order: 1
---

<div class="neon-header">
  <h1 class="neon-title">HELLO-CICD</h1>
  <p class="neon-subtitle">Enterprise-Grade Flask Subscription Platform</p>
</div>

## 📋 Quick Index

| Section | Description |
|---------|-------------|
| [Overview](docs/overview.md) | Project introduction & key features |
| [Architecture](docs/architecture/overview.md) | System design & component diagrams |
| [Development Guide](docs/development/setup.md) | Setup instructions for all platforms |
| [Deployment](docs/deployment/azure.md) | Azure deployment & CI/CD pipeline |
| [API Reference](docs/architecture/api.md) | Endpoints & data models |
| [Contributing](docs/guides/contributing.md) | Development workflow & standards |

---

## 🎯 Core Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Backend runtime |
| **Flask 3.x** | Web framework |
| **Flask-SQLAlchemy** | Database ORM |
| **Azure SQL Database** | Production database |
| **Gunicorn** | WSGI server |
| **Docker** | Containerization |
| **Azure Container Apps** | Cloud deployment |
| **GitHub Actions** | CI/CD pipeline |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/hello-cicd.git
cd hello-cicd

# Setup development environment
./scripts/setup.sh

# Run locally
flask run

# Build Docker image
docker build -t hello-cicd:latest .
```

---

## 📦 Deployment Pipeline

```
GitHub Push → GitHub Actions → Azure Container Registry → Azure Container Apps
                              ↓                                    ↓
                    Health Check & Verification          Azure SQL Database
```

---

## 🔐 Admin Panel

The application includes a protected admin panel for managing newsletter subscribers.

**URL:** `/admin/login`

**Features:**
| Feature | Description |
|---------|-------------|
| Authentication | Session-based login with password hashing |
| Subscriber List | View all subscribers with sorting options |
| Sorting | By date, name, or email (ascending/descending) |
| Edit | Modify subscriber name and email |
| Delete | Remove individual or multiple subscribers |
| Export | Copy emails to clipboard (Outlook format) |

**Database Tables:**
- `users` - Admin user accounts
- `subscribers` - Newsletter subscribers

---

## 📧 Nyhetsbrev

Plattformen erbjuder 5 olika nyhetsbrev:

| Nyhetsbrev | Beskrivning |
|------------|-------------|
| 🥗 **Kost & Näring** | Kraftfulla recept, kosttips och näringslära för maximal energi |
| 🧠 **Mindset** | Mental styrka, motivation och fokus för att nå nästa nivå |
| 🔬 **Kunskap & Forskning** | Vetenskapligt grundade tips - träna smartare, inte bara hårdare |
| 💪 **Veckans Pass** | Nya träningspass varje vecka - HIIT, styrka och stretch |
| 🤖 **Träna med Jaine** | AI-tränare som skapar personliga träningsprogram |

---

## 💻 Supported Platforms

| OS | Version | Shell | Status |
|----|---------|-------|--------|
| macOS | Monterey (12.x+) | zsh/bash | ✅ Supported |
| Linux | CachyOS | fish/zsh | ✅ Supported |
| Windows | 11 | PowerShell | ✅ Supported |

---

## 📊 Project Links

- **Repository**: [GitHub](https://github.com/your-org/hello-cicd)
- **Issues**: [Jira Board](https://your-org.atlassian.net/browse/HELLO)
- **Azure Portal**: [Production](https://portal.azure.com)
- **CI/CD**: [GitHub Actions](https://github.com/your-org/hello-cicd/actions)

---

<div class="neon-footer">
  <p>Built with ⚡ by the Hello-CICD Team</p>
  <p>Licensed under MIT</p>
</div>

<style>
.neon-header {
  text-align: center;
  padding: 3rem 0;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid #ff00ff33;
}

.neon-title {
  font-family: 'Courier New', monospace;
  font-size: 3.5rem;
  font-weight: bold;
  color: #fff;
  text-shadow:
    0 0 5px #ff00ff,
    0 0 10px #ff00ff,
    0 0 20px #ff00ff,
    0 0 40px #ff00ff,
    0 0 80px #ff00ff;
  margin: 0;
  letter-spacing: 4px;
}

.neon-subtitle {
  font-family: 'Courier New', monospace;
  font-size: 1.2rem;
  color: #00ffff;
  text-shadow:
    0 0 5px #00ffff,
    0 0 10px #00ffff;
  margin-top: 0.5rem;
}

.neon-footer {
  text-align: center;
  padding: 2rem;
  margin-top: 3rem;
  border-top: 1px solid #333;
  color: #888;
  font-family: 'Courier New', monospace;
}
</style>
