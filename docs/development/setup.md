---
layout: default
title: Development Setup
nav_order: 1
parent: Development
---

<div class="neon-page-header">
  <h1 class="neon-heading">💻 DEVELOPMENT SETUP</h1>
</div>

## Platform Selection

| Platform | Status | Shell |
|----------|--------|-------|
| [macOS Monterey+](#-macos-setup) | ✅ Supported | zsh/bash |
| [Linux CachyOS](#-linux-cachyos-setup) | ✅ Supported | fish/zsh |
| [Windows 11](#-windows-11-setup) | ✅ Supported | PowerShell |

---

## Prerequisites

| Tool | macOS | Linux | Windows |
|------|-------|-------|---------|
| Python 3.11+ | ✅ | ✅ | ✅ |
| Git | ✅ | ✅ | ✅ |
| Docker Desktop | ✅ | ✅ | ✅ |
| Azure CLI | ✅ | ✅ | ✅ |

### Database Driver (Automatic)

The application uses SQLAlchemy with `pymssql` driver, which is a pure Python implementation. No external ODBC drivers are required - all dependencies are installed via pip.

---

## Common Setup

```bash
# Clone the repository
git clone https://github.com/your-org/hello-cicd.git
cd hello-cicd
```

---

## 🍎 macOS Setup

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Dependencies

```bash
# Install Python 3.11+
brew install python@3.11

# Install Docker Desktop
brew install --cask docker

# Install Azure CLI
brew install azure-cli

# Install Git
brew install git
```

### Step 3: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run Application

```bash
# Development mode
flask run --debug

# Or using Gunicorn
gunicorn --bind 0.0.0.0:5000 --reload wsgi:app
```

### Step 5: Verify Installation

```bash
# Check Python version
python --version  # Should be 3.11+

# Check Flask installation
flask --version

# Run application
curl http://localhost:5000
# Should return HTML homepage
```

---

## 🐧 Linux CachyOS Setup

### Step 1: Install System Dependencies

```bash
# Update package list
sudo pacman -Syu

# Install Python and development tools
sudo pacman -S python311 python-pip python-virtualenv git

# Install Docker
sudo pacman -S docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Step 2: Setup Python Environment (with fish shell)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate.fish

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run Application

```bash
# Development mode
flask run --debug --host 0.0.0.0

# Or using Gunicorn
gunicorn --bind 0.0.0.0:5000 --reload wsgi:app
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version

# Check Docker
docker --version

# Run application
curl http://localhost:5000
```

---

## 🪟 Windows 11 Setup

### Step 1: Install Prerequisites

**Install using Winget:**

```powershell
# Install Python
winget install Python.Python.3.11

# Install Git
winget install Git.Git

# Install Docker Desktop
winget install Docker.DockerDesktop

# Install Azure CLI
winget install Microsoft.AzureCLI
```

### Step 2: Setup Python Environment

**Open PowerShell as Administrator:**

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run Application

```powershell
# Development mode
flask run --debug --host 0.0.0.0

# Or using Gunicorn
gunicorn --bind 0.0.0.0:5000 --reload wsgi:app
```

### Step 4: Verify Installation

```powershell
# Check Python version
python --version

# Check Flask
flask --version

# Test application
Invoke-WebRequest http://localhost:5000
```

---

## 🐳 Docker Development

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - SECRET_KEY=dev-secret-key
    volumes:
      - .:/app
    command: flask run --host 0.0.0.0 --debug
```

### Run with Docker

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🔧 IDE Configuration

### VS Code Recommended Extensions

| Extension | Purpose |
|-----------|---------|
| Python | Language support |
| Pylance | Type checking |
| Docker | Container support |
| Azure Tools | Azure integration |
| GitLens | Git enhancements |

### PyCharm Configuration

1. Open project in PyCharm
2. Configure Python interpreter (venv)
3. Set run configuration to Flask
4. Enable Docker integration

---

## ✅ Verification Checklist

| Check | Command | Expected |
|-------|---------|----------|
| Python installed | `python --version` | 3.11+ |
| Pip working | `pip --version` | Latest |
| Flask working | `flask --version` | 3.x |
| Dependencies | `pip list` | All installed |
| App runs | `curl localhost:5000` | HTML response |
| Docker | `docker --version` | 20.x+ |
| Azure CLI | `az --version` | 2.x+ |

---

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process
kill <PID>
```

#### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Or on Windows, run Docker Desktop as administrator
```

---

## 📚 Next Steps

- [Local Development Workflow](workflow.md)
- [Running Tests](testing.md)
- [Code Style Guide](style-guide.md)
- [Deployment Guide](../deployment/azure.md)

---

[← Development Home](README.md) | [Next: Development Workflow →](workflow.md)

<style>
.neon-page-header {
  background: linear-gradient(90deg, #0a0a0a 0%, #1a2e1a 50%, #0a0a0a 100%);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #00ff0033;
}

.neon-heading {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #fff;
  text-shadow:
    0 0 10px #00ff00,
    0 0 20px #00ff00;
  margin: 0;
}
</style>
