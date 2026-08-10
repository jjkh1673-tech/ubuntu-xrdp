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

This fork now includes **Hermes AI Agent** - a built-in intelligent assistant that provides:
- ✅ **Zero-setup mode** - Works immediately without any API keys
- ✅ **System assistance** - Help with XRDP, Ubuntu, Docker, and more
- ✅ **Desktop integration** - Launch from applications menu with one click
- ✅ **Optional cloud AI** - Add API key for full AI capabilities
- ✅ **Interactive mode** - Chat naturally with the agent

> **No extra setup required!** Just build and run - Hermes is ready to help.

---

## 🎤 Hermes AI Agent - Quick Start

### Launch Hermes

**From Terminal:**
```bash
hermes-agent
```

**From Desktop:**
Click the **Hermes AI Agent** icon in your Applications menu.

### Simple Commands

```
hermes-agent                    # Start interactive chat
hermes-agent "system info"     # Get system information
hermes-agent "help"            # Show help
hermes-agent status            # Check agent status
hermes-agent setup             # Set up desktop integration
```

### Example Interactions

```
You: system info
Hermes: Returns detailed system information

You: memory
Hermes: Shows RAM and disk usage

You: xrdp help
Hermes: Connection troubleshooting guide

You: help
Hermes: Lists all available commands
```

---

## 🖥️ hermes-agent Features

### Zero-Setup Local Mode (Default)

Hermes works **out of the box** without any API keys:

| Feature | Description |
|---------|-------------|
| System Info | Get OS, memory, disk, Docker info |
| Resource Monitor | Check CPU, RAM, disk space |
| XRDP Help | Connection guides, troubleshooting |
| Desktop Help | XFCE4 tips, application installation |
| Development Help | Python, Node.js, Git assistance |
| Troubleshooting | Common fixes for errors |

### Optional Cloud AI Mode

Want full AI intelligence? Add an API key:

```bash
# OpenAI
export HERMES_OPENAI_API_KEY='sk-your-key-here'

# Anthropic  
export HERMES_ANTHROPIC_API_KEY='your-key-here'

# Then restart hermes-agent
hermes-agent
```

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
3. Click to launch

---

## 🎤 Using Hermes AI Agent

### Interactive Mode

```
$ hermes-agent

══════════════════════════════════════════════════════════
  🎤 HERMES AI AGENT - Interactive Mode
  Type 'help' for commands, 'quit' to exit
  Mode: LOCAL (type 'status' for details)
══════════════════════════════════════════════════════════

You: help

Hermes: Shows help menu with all commands

You: system info

Hermes: Returns detailed system information

You: quit
```

### Quick Commands

```bash
# Get system information
hermes-agent "system info"

# Check resources
hermes-agent memory
hermes-agent disk

# XRDP help
hermes-agent xrdp
hermes-agent connect

# Troubleshooting
hermes-agent error
hermes-agent problem

# Development help
hermes-agent python
hermes-agent install package
```

### Desktop Integration

Hermes creates a desktop shortcut automatically during build:

- **Icon**: Purple "H" logo in Applications menu
- **Launch**: Click to open terminal with Hermes
- **Accessibility**: Always available from menu

---

## 🖥️ Supported Operating Systems

### 🐧 Linux Distributions

#### 1. Ubuntu 24.04 LTS (DEFAULT ✅)

| Attribute | Value |
|-----------|-------|
| **Best for** | General use, stability, AI/ML, development, beginners |
| **Compatibility** | ✅ Default - Fully Tested |
| **Why choose it** | LTS support, huge community, Docker-native |
| **Official Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 2. Debian 12 (Bullseye/Bookworm)

| Attribute | Value |
|-----------|-------|
| **Best for** | Server use, minimal setups |
| **Compatibility** | ✅ Compatible |
| **Why choose it** | Rock-solid stability |
| **Official Download** | [debian.org/download](https://www.debian.org/download) |

---

#### 3. Kali Linux (Security Testing)

| Attribute | Value |
|-----------|-------|
| **Best for** | Penetration testing, CTF, security labs |
| **Compatibility** | ⚠️ Experimental |
| **Why choose it** | Pre-installed security tools |
| **Official Download** | [kali.org/get-kali](https://www.kali.org/get-kali/) |

---

### 🪟 Windows Options

#### 4. Windows 10

> ⚠️ Requires VM or special setup (not native Docker)

| Attribute | Value |
|-----------|-------|
| **Best for** | Windows app testing, legacy software |
| **Compatibility** | ⚠️ Special setup required |
| **Official ISO** | [microsoft.com/windows10](https://www.microsoft.com/software-download/windows10) |

---

#### 5. Windows 11 (Latest)

| Attribute | Value |
|-----------|-------|
| **Best for** | Latest Windows features, AI-enabled apps |
| **Compatibility** | ⚠️ Special setup required |
| **Official ISO** | [microsoft.com/windows11](https://www.microsoft.com/software-download/windows11) |

---

### 🍎 macOS Options

#### 6. macOS Sonoma (Latest)

> ⚠️ Only on Apple Silicon hardware

| Attribute | Value |
|-----------|-------|
| **Best for** | iOS/macOS development |
| **Compatibility** | ⚠️ Apple hardware only |
| **Official** | [apple.com/macos](https://apple.com/macos) |

---

### ⚡ Powerful Unix Systems for AI & Trending Sectors

#### 7. Alpine Linux (AI/ML Lightweight)

| Attribute | Value |
|-----------|-------|
| **Best for** | Lightweight AI containers, microservices |
| **Official** | [alpinelinux.org](https://alpinelinux.org/) |

---

#### 8. Fedora AI (Artificial Intelligence Focus)

| Attribute | Value |
|-----------|-------|
| **Best for** | AI/ML development, PyTorch, TensorFlow |
| **Official** | [fedoraproject.org](https://fedoraproject.org/) |

---

#### 9. Rocky Linux / AlmaLinux (Enterprise AI)

| Attribute | Value |
|-----------|-------|
| **Best for** | Enterprise AI deployments |
| **Official** | [rockylinux.org](https://rockylinux.org/) |

---

#### 10. Arch Linux / Manjaro (Cutting Edge)

| Attribute | Value |
|-----------|-------|
| **Best for** | Latest packages, rolling release |
| **Official** | [archlinux.org](https://archlinux.org/) |

---

#### 11. NixOS (Reproducible AI Environments)

| Attribute | Value |
|-----------|-------|
| **Best for** | Reproducible AI/ML environments |
| **Official** | [nixos.org](https://nixos.org/) |

---

#### 12. OpenSUSE (AI Development)

| Attribute | Value |
|-----------|-------|
| **Best for** | AI development, containers |
| **Official** | [opensuse.org](https://www.opensuse.org/) |

---

## 📊 Quick Comparison Table

| OS | Docker Base | AI/ML Ready | Beginner Friendly | Hermes Support |
|----|-------------|-------------|-------------------|----------------|
| **Ubuntu 24.04 LTS** | ✅ Yes | ✅ Excellent | ✅ Yes | ✅ Full |
| Debian 12 | ✅ Yes | ✅ Good | ⚠️ Moderate | ✅ Full |
| Kali Linux | ✅ Yes | ⚠️ Tools only | ⚠️ Learning curve | ✅ Full |
| Windows 10/11 | ❌ VM needed | ⚠️ Via WSL2 | ✅ Yes | ❌ Limited |
| macOS | ❌ Apple only | ✅ Good | ✅ Yes | ❌ Limited |
| Alpine Linux | ✅ Yes | ⚠️ Lightweight | ⚠️ Advanced | ✅ Full |
| Fedora | ✅ Yes | ✅ Excellent | ⚠️ Moderate | ✅ Full |
| Rocky/AlmaLinux | ✅ Yes | ✅ Enterprise | ⚠️ Server-focused | ✅ Full |
| Arch/Manjaro | ⚠️ Community | ✅ Cutting-edge | ⚠️ Rolling release | ✅ Full |
| NixOS | ⚠️ Experimental | ✅ Reproducible | ⚠️ Unique paradigm | ✅ Full |

---

## 📁 Files in This Repository

```
ubuntu-xrdp/
├── Dockerfile           # ← Main config (Ubuntu 24.04 + Hermes AI)
├── hermes-agent         # ← Built-in AI assistant (Python script)
├── start.sh             # Container startup script
├── pulse-client.conf    # Audio config for XRDP
└── README.md            # This file
```

### Which File Does What?

| File | Purpose | Modify For |
|------|---------|------------|
| **Dockerfile** | Base OS, packages, Hermes integration | Change OS, add packages |
| **hermes-agent** | AI assistant (local + cloud mode) | Customize AI responses |
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

# Launch Hermes
docker exec -it xrdp-desktop hermes-agent

# Stop container
docker stop xrdp-desktop

# Remove container
docker rm xrdp-desktop
```

---

## 🎤 Hermes AI Agent Commands

```bash
# Launch interactive mode
hermes-agent

# Single query
hermes-agent "system info"

# Check status
hermes-agent status

# Show help
hermes-agent help

# Setup desktop integration
hermes-agent setup
```

### Hermes Topics

| Query | Response |
|-------|----------|
| `system info` | OS, version, desktop environment details |
| `memory` / `disk` | RAM and storage usage |
| `docker` | Container and image information |
| `xrdp` / `connect` | RDP connection guide |
| `help` | All available commands |
| `troubleshoot` | Common fixes |
| `python` / `node` | Development setup help |
| `install <pkg>` | Package installation guide |

---

## 🔐 Security Notes

1. **Default password is `root`** - Change it for production
2. **Hermes runs locally by default** - No data leaves your container
3. **Cloud API keys are optional** - Only needed for full AI features
4. **Windows/macOS** require separate licensing

### Changing Default Password

```bash
docker build --build-arg ROOT_PASSWORD="YourSecurePassword123!" -t xrdp .
```

---

## 🐛 Troubleshooting

### Hermes Not Found

```bash
# Check if Hermes is installed
which hermes-agent

# If not, the container may need rebuilding
docker build -t xrdp .
```

### Hermes Not Responding

```bash
# Check Python is available
python3 --version

# Test Hermes directly
python3 /usr/local/bin/hermes-agent status
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
4. Test thoroughly (including Hermes functionality)
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
| This Repository | [github.com/jjkh1673-tech/ubuntu-xrdp](https://github.com/jjkh1673-tech/ubuntu-xrdp) |

---

## 🏁 Summary

| Feature | Details |
|---------|---------|
| **Default OS** | Ubuntu 24.04 LTS |
| **Desktop** | XFCE4 |
| **Remote Access** | RDP (port 3389) |
| **AI Agent** | Hermes (built-in, zero-setup) |
| **Main Config** | `Dockerfile` |
| **AI Agent** | `hermes-agent` |
| **Quick Build** | `docker build -t xrdp .` |
| **Quick Run** | `docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp` |
| **Launch Hermes** | `hermes-agent` |

---

> **💡 TIP**: After connecting via RDP, click the Hermes icon in Applications menu or type `hermes-agent` in terminal to start chatting with your AI assistant!
