---
layout: default
title: Development
nav_order: 3
has_children: true
---

<div class="neon-page-header">
  <h1 class="neon-heading">💻 DEVELOPMENT</h1>
</div>

## Getting Started

Setup instructions for all supported platforms: macOS, Linux CachyOS, and Windows 11.

## Contents

| Page | Description |
|------|-------------|
| [Setup Guide](development/setup.md) | Platform-specific installation |
| [Development Workflow](development/workflow.md) | Daily development process |
| [Testing Guide](development/testing.md) | Running and writing tests |
| [Code Style](development/style-guide.md) | Coding standards |

## Platform Support Matrix

| OS | Version | Shell | Status |
|----|---------|-------|--------|
| macOS | Monterey (12+) | zsh/bash | ✅ Supported |
| Linux | CachyOS | fish/zsh | ✅ Supported |
| Windows | 11 | PowerShell | ✅ Supported |

## Quick Links

- [← Back to Home](README.md)
- [Architecture →](architecture/overview.md)
- [Deployment →](deployment/azure.md)

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
