# Ubuntu XRDP Desktop in Docker

> **Multi-Purpose Linux Environment Deployment with Remote Desktop + Built-in Hermes AI Agent**

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Default-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com)
[![XRDP](https://img.shields.io/badge/XRDP-0.9.x-green.svg)](https://github.com/neutrinolabs/xrdp)
[![Hermes AI](https://img.shields.io/badge/Hermes-AI_Agent-purple.svg)](https://github.com/jjkh1673-tech/ubuntu-xrdp)

---

## 🚀 What Is This Project?

This project provides a **Docker container with a full Ubuntu Linux desktop environment** that you can access remotely using Microsoft's Remote Desktop Protocol (RDP). Think of it as a virtual Ubuntu computer that runs inside Docker and can be accessed from Windows, macOS, or another Linux machine.

### 🎤 NEW: Built-in Hermes AI Agent!

This fork now includes **Hermes AI Agent** - a built-in intelligent assistant with:

- ✅ **First-Run Setup Wizard** - Guides you through API key configuration
- ✅ **Zero-Setup Local Mode** - Works immediately without API keys
- ✅ **Secure Credential Storage** - API keys stored encrypted in ~/.hermes/
- ✅ **One-Click Desktop Launch** - Click icon in Applications menu
- ✅ **Optional Cloud AI** - Add API key once, get full AI forever
- ✅ **High Performance** - Optimized for fast responses

> **No extra setup required!** Just build, run, and type `hermes-agent`. First time it will guide you to set up API key if you want full AI.

---

## 🎤 Hermes AI Agent - Quick Setup Guide

### First Time Launch (Automatic Setup Wizard)

When you first run Hermes, it automatically launches a **setup wizard**:

```bash
hermes-agent
```

**What happens:**
1. ❓ It asks which AI provider you want (OpenAI or Anthropic)
3. 🔑 It asks for your API key (or you can skip for local mode)
4. ✅ It validates the key and saves it securely
5. 🚀 You're ready! Full AI capabilities enabled

**That's it!** No manual configuration needed.

---

### Quick Commands

```bash
# First time setup (wizard will guide you)
hermes-agent

# Or run setup explicitly
hermes-agent setup

# Check status
hermes-agent status

# Quick query
hermes-agent "system info"

# Launch interactive mode
hermes-agent
```

---

### Example First-Run Session

```
$ hermes-agent

══════════════════════════════════════════════════════════════
  🎤 HERMES AI AGENT - First Time Setup
══════════════════════════════════════════════════════════════

  Welcome! Let's configure your AI assistant in 2 minutes.
  This setup only needs to be done ONCE.

──────────────────────────────────────────────────────────────
  STEP 1: Choose Your AI Provider
──────────────────────────────────────────────────────────────

  Select which AI service you want to use:

  [1] OpenAI (GPT-4o-mini) - Fast, affordable, excellent quality
  [2] Anthropic (Claude Haiku) - Fast, safe, great reasoning
  [3] Skip - Use local mode only (no API key needed)

  Enter choice [1/2/3]: 1

  ✓ Selected: OpenAI

──────────────────────────────────────────────────────────────
  STEP 2: Enter OpenAI API Key
──────────────────────────────────────────────────────────────

  To get an API key:
  1. Go to: https://platform.openai.com/api-keys
  2. Sign up/log in and create a new API key
  3. Copy the key (starts with 'sk-')

  ⚠️  Your key is stored securely and never shared.

  Enter your API key (or 'skip' to use local mode):
  API Key: ********************************

  ✓ API key format looks valid
  ✓ Testing connection...
  ✓ Connection successful!

──────────────────────────────────────────────────────────────
  STEP 3: Saving Configuration...
──────────────────────────────────────────────────────────────

  ✓ API key saved securely
  ✓ Default provider configured
  ✓ Setup marker created

══════════════════════════════════════════════════════════════
  ✅ SETUP COMPLETE!
══════════════════════════════════════════════════════════════

  Provider: OpenAI
  Model: gpt-4o-mini

  Hermes AI Agent is now ready with FULL AI capabilities!
  Just type 'hermes-agent' and start chatting.

══════════════════════════════════════════════════════════════
```

---

### After Setup - Using Hermes

```
$ hermes-agent

══════════════════════════════════════════════════════════════
  🎤 HERMES AI AGENT - Interactive Mode
  Type 'help' for commands, 'quit' to exit
  Mode: OPENAI
══════════════════════════════════════════════════════════════

You: system info

Hermes: Returns detailed system information with full AI

You: help me set up python

Hermes: Provides intelligent guidance with full AI understanding

You: what can I do with this desktop?

Hermes: Explains all features with full AI knowledge

You: quit
```

---

## 🎤 Hermes AI Agent Features

### Automatic Setup Wizard

| Feature | Description |
|---------|-------------|
| **Interactive Prompts** | Clear step-by-step guided setup |
| **Provider Selection** | Choose OpenAI or Anthropic |
| **Key Validation** | Tests API key before saving |
| **Secure Storage** | Saves to ~/.hermes/credentials.json (permissions 600) |
| **Environment Variable Support** | Also reads from env vars if set |

### Zero-Setup Local Mode

Works immediately without any API keys:

| Feature | Description |
|---------|-------------|
| System Info | OS, memory, disk, Docker info |
| Resource Monitor | CPU, RAM, disk space |
| XRDP Help | Connection guides, troubleshooting |
| Desktop Help | XFCE4 tips, application installation |
| Development Help | Python, Node.js, Git assistance |
| Troubleshooting | Common fixes for errors |

### Cloud AI Mode (Optional)

Add API key once, get full AI forever:

```bash
# Setup wizard (recommended)
hermes-agent setup

# Or manually set environment variable
export HERMES_OPENAI_API_KEY='sk-your-key-here'
export HERMES_ANTHROPIC_API_KEY='your-key-here'

# Then run Hermes
hermes-agent
```

**Supported Providers:**
- **OpenAI** (GPT-4o-mini) - Fast, affordable, excellent quality
- **Anthropic** (Claude Haiku) - Fast, safe, great reasoning

---

## 🚀 Quick Start (Copy-Paste Guide)

### Prerequisites

- ✅ **Docker installed** on your system
- ✅ **Terminal/command prompt** access
- ✅ **RDP client** (Windows Remote Desktop, Remmina for Linux, Microsoft Remote Desktop for macOS)

### Step 1: Clone This Repository

```bash
git clone https://github.com/jjkh1673-tech/ubuntu-xrdp.git
cd ubuntu-xrdp
```

### Step 2: Build the Docker Image

```bash
docker build -t xrdp .
```

> ⏱️ **Time**: First build takes 3-10 minutes depending on your internet speed.

### Step 3: Run the Container

```bash
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

### Step 4: Connect via RDP

1. Open your RDP client
2. Connect to: `localhost:3389` (or your machine's IP address)
3. Login with:
   - **Username**: `root`
   - **Password**: `root`

### Step 5: Launch Hermes AI Agent

Once connected to the desktop:

**Option 1 - Terminal:**
```bash
hermes-agent
```

**Option 2 - Desktop Menu:**
1. Open Applications menu
2. Find "Hermes AI Agent"
3. Click to launch (first time = setup wizard)

---

## 📁 Files in This Repository

```
ubuntu-xrdp/
├── Dockerfile           # ← Main config (Ubuntu 24.04 + Hermes AI)
├── hermes-agent         # ← Built-in AI assistant (Python script)
│                          #   - First-run setup wizard included
│                          #   - Secure credential storage
│                          #   - Local + Cloud AI modes
├── start.sh             # Container startup script
├── pulse-client.conf    # Audio config for XRDP
└── README.md            # This file
```

### Which File Does What?

| File | Purpose | Modify For |
|------|---------|------------|
| **Dockerfile** | Base OS, packages, Hermes integration | Change OS, add packages |
| **hermes-agent** | AI assistant with setup wizard | Customize AI responses, providers |
| **start.sh** | Service startup | Change service order |
| **pulse-client.conf** | Audio configuration | Audio troubleshooting |

---

## 🛠️ Commands Reference

```bash
# Build the image
docker build -t xrdp .

# Build with custom password
docker build --build-arg ROOT_PASSWORD="MySecurePass123" -t xrdp .

# Run the container
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp

# Check running containers
docker ps

# View container logs
docker logs xrdp-desktop

# Enter container
docker exec -it xrdp-desktop bash

# Launch Hermes (first time = setup wizard)
docker exec -it xrdp-desktop hermes-agent

# Launch Hermes with query
docker exec -it xrdp-desktop hermes-agent "system info"

# Check Hermes status
docker exec -it xrdp-desktop hermes-agent status

# Stop container
docker stop xrdp-desktop

# Remove container
docker rm xrdp-desktop

# Full reset (rebuild from scratch)
docker stop xrdp-desktop && docker rm xrdp-desktop && docker rmi xrdp && docker build -t xrdp . && docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

---

## 🎤 Hermes AI Agent Commands

| Command | Description |
|---------|-------------|
| `hermes-agent` | Launch interactive mode (setup wizard on first run) |
| `hermes-agent setup` | Run setup wizard explicitly |
| `hermes-agent status` | Check agent configuration status |
| `hermes-agent help` | Show help commands |
| `hermes-agent "query"` | Quick query mode |

### Interactive Mode Commands

| Command | Description |
|---------|-------------|
| `help` | Show all commands |
| `status` | Check agent status |
| `setup` | Reconfigure API key |
| `quit` | Exit Hermes |

### Query Examples

```
hermes-agent "system info"
hermes-agent "memory"
hermes-agent "docker"
hermes-agent "xrdp help"
hermes-agent "how do I install python"
hermes-agent "troubleshoot connection"
```

---

## 🔐 Security

### API Key Storage

- API keys are stored in `~/.hermes/credentials.json`
- File permissions set to `600` (only owner can read/write)
- Keys are also set as environment variables for current session
- Keys are NEVER logged or shared

### Changing Default Password

```bash
docker build --build-arg ROOT_PASSWORD="YourSecurePassword123!" -t xrdp .
```

### Resetting Hermes Configuration

```bash
# Reset all Hermes settings
hermes-agent setup
# (This clears old config and starts fresh)
```

---

## 🐛 Troubleshooting

### Hermes Not Found

```bash
# Check if Hermes is installed
which hermes-agent

# If not found, container needs rebuilding
docker build -t xrdp .
```

### Setup Wizard Not Appearing

```bash
# Force reset and run setup again
hermes-agent setup
```

### API Key Not Working

```bash
# Check if key is stored
cat ~/.hermes/credentials.json

# Reconfigure
hermes-agent setup
```

### Connection Issues

1. Verify container is running: `docker ps`
2. Check port mapping: `docker port xrdp-desktop`
3. Try: `localhost:3389` or `127.0.0.1:3389`

### Black Screen After Login

1. Check XFCE4: `docker exec xrdp-desktop dpkg -l | grep xfce4`
2. Check session: `docker exec xrdp-desktop cat /root/.xsession`
3. Restart container: `docker restart xrdp-desktop`

---

## 🤝 Contributing

Contributions welcome! When contributing:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test Hermes functionality
5. Submit a pull request

---

## 📄 License

Based on [hopingboyz/debianxrdp](https://github.com/hopingboyz/debianxrdp)

Hermes AI Agent is included as a built-in feature for user assistance.

---

## 🔗 Useful Links

| Resource | Link |
|----------|------|
| Docker Documentation | [docs.docker.com](https://docs.docker.com/) |
| XRDP Project | [github.com/neutrinolabs/xrdp](https://github.com/neutrinolabs/xrdp) |
| XFCE4 Desktop | [xfce.org](https://xfce.org/) |
| Ubuntu Download | [ubuntu.com/download](https://ubuntu.com/download) |
| OpenAI API Keys | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Anthropic API Keys | [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) |
| This Repository | [github.com/jjkh1673-tech/ubuntu-xrdp](https://github.com/jjkh1673-tech/ubuntu-xrdp) |

---

## 🏁 Summary

| Feature | Details |
|---------|---------|
| **Default OS** | Ubuntu 24.04 LTS |
| **Desktop** | XFCE4 |
| **Remote Access** | RDP (port 3389) |
| **AI Agent** | Hermes (built-in, setup wizard) |
| **Main Config** | `Dockerfile` |
| **AI Agent** | `hermes-agent` |
| **Quick Build** | `docker build -t xrdp .` |
| **Quick Run** | `docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp` |
| **Launch Hermes** | `hermes-agent` (first time = setup wizard) |

---

> **💡 TIP**: After connecting via RDP, type `hermes-agent` in terminal. First time it will guide you through API key setup for full AI. After that, just type `hermes-agent` anytime to chat with AI!
