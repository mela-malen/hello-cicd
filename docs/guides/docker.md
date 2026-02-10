---
layout: default
title: Docker Guide
nav_order: 2
parent: Guides
---

<div class="neon-page-header">
  <h1 class="neon-heading">🐳 DOCKER GUIDE</h1>
</div>

## Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:app"]
```

## Building Images

```bash
# Build local image
docker build -t hello-cicd:latest .

# Build with specific tag
docker build -t hello-cicd:v1.2.0 .

# Build and push to ACR
az acr build \
  --registry helloCicdRegistry \
  --image hello-cicd:${{ github.sha }} .
```

## Running Containers

```bash
# Run detached
docker run -d -p 5000:5000 --name hello-cicd hello-cicd:latest

# Run with environment variables
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret \
  hello-cicd:latest

# Run with volume mount
docker run -d \
  -p 5000:5000 \
  -v $(pwd):/app \
  hello-cicd:latest
```

## Docker Compose

```yaml
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
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

volumes:
  redis-data:
```

[← Guides](README.md) | [Next: Contributing →](contributing.md)

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
