---
layout: default
title: Custom Domain Setup
nav_order: 4
parent: Guides
---

<div class="neon-page-header">
  <h1 class="neon-heading">🌐 CUSTOM DOMAIN SETUP</h1>
</div>

## Problem

| URL | Status | Issue |
|-----|--------|-------|
| `https://ca-hello-cicd.calmsky-c5b24015.swedencentral.azurecontainerapps.io` | ✅ Works | Default FQDN |
| `http://deploj.se` | ❌ 404 | Custom domain not configured |

## Solution: Add Custom Domain to Azure Container App

### Step 1: Get Container App FQDN

```bash
az containerapp show \
  --name hello-cicd-app \
  --resource-group hello-cicd-rg \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv

# Result: ca-hello-cicd.calmsky-c5b24015.swedencentral.azurecontainerapps.io
```

### Step 2: Configure Custom Domain in Azure Portal

1. Go to **Azure Portal** → **Container Apps** → **hello-cicd-app**
2. Click **Custom domains** (left menu)
3. Click **Add custom domain**
4. Enter: `deploj.se`
5. Select **TLS certificate**
6. Click **Add**

### Step 3: Add DNS Record

| Record Type | Name | Value | TTL |
|-------------|------|-------|-----|
| A | @ | Your Container App IP | 600 |

**Get IP Address:**

```bash
# Get the IP from your Container App ingress
az containerapp show \
  --name hello-cicd-app \
  --resource-group hello-cicd-rg \
  --query "ipAddress" \
  --output tsv
```

### Step 4: Verify Domain Configuration

```bash
# Check DNS
dig deploj.se +short

# Test HTTPS
curl -v https://deploj.se/
```

---

## DNS Configuration Options

### Option 1: A Record (Recommended)

```
Type: A
Name: @
Value: <CONTAINER_APP_IP>
TTL: 600
```

### Option 2: CNAME Record

```
Type: CNAME
Name: @
Value: ca-hello-cicd.calmsky-c5b24015.swedencentral.azurecontainerapps.io
TTL: 600
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 Azure Container App | Configure custom domain in portal |
| SSL Certificate Error | Upload certificate in custom domain blade |
| DNS Not Resolving | Wait 1-24 hours for propagation |
| Connection Refused | Check Container App ingress is enabled |

---

## Azure CLI Command Reference

```bash
# List custom domains
az containerapp hostname list \
  --name hello-cicd-app \
  --resource-group hello-cicd-rg

# Delete custom domain
az containerapp hostname delete \
  --name hello-cicd-app \
  --resource-group hello-cicd-rg \
  --hostname deploj.se
```

---

[← Troubleshooting](troubleshooting.md)

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
