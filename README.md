# Ubuntu XRDP Desktop (built-in ai)

> **Multi-Purpose Linux Environment Deployment with Remote Desktop + Built-in Hermes AI Desktop**

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Default-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com)
[![XRDP](https://img.shields.io/badge/XRDP-0.9.x-green.svg)](https://github.com/neutrinolabs/xrdp)
[![Hermes AI](https://img.shields.io/badge/Hermes-AI_Desktop-purple.svg)](https://github.com/jjkh1673-tech/ubuntu-xrdp)

---

## 🚀 What Is This Project?

This project provides a **Docker container with a full Ubuntu Linux desktop environment** that you can access remotely using Microsoft's Remote Desktop Protocol (RDP). Think of it as a virtual Ubuntu computer that runs inside Docker and can be accessed from Windows, macOS, or another Linux machine.

### 🎤 NEW: Hermes AI Desktop (Built-in AI)

This fork now includes **Hermes AI Desktop** - a beautiful, Claude Desktop-like AI chat application built right in:

- ✅ **Beautiful GUI** - Modern dark theme interface like Claude Desktop
- ✅ **First-Run API Key Wizard** - Guides you step-by-step to set up
- ✅ **Multiple AI Models** - Access to various models via gateway
- ✅ **Chat Interface** - Real-time streaming chat with AI
- ✅ **Tool Integration** - File operations (read, write, delete, list)
- ✅ **Desktop Icon** - Launch from Applications menu
- ✅ **Terminal Launch** - Type `hermes` in terminal
- ✅ **Cross-Platform** - Works on any OS with limitations (see below)

> **No extra setup required!** Just build, run, connect via RDP, and launch Hermes from the desktop icon or terminal.

---

## ⚠️ IMPORTANT: OS Compatibility

| Operating System | Hermes AI Desktop Support | Notes |
|------------------|---------------------------|-------|
| **Ubuntu Linux (Default)** | ✅ Full Support | Primary target platform |
| **Debian Linux** | ✅ Full Support | Compatible |
| **Kali Linux** | ⚠️ Experimental | May need adjustments |
| **Windows** | ❌ Not Supported | Cannot run Linux GUI apps directly. Use WSL2 or RDP into this container |
| **macOS** | ⚠️ Limited | Cannot run directly. Use Docker with VNC or RDP client |

### For Windows Users

Since Windows cannot directly run Linux GUI applications, you have two options:

1. **Use RDP to connect to this container** (recommended)
   - Build and run this Docker container
   - Connect via Windows Remote Desktop to `localhost:3389`
   - Use Hermes AI Desktop inside the Linux desktop

2. **Use WSL2** (Windows Subsystem for Linux)
   - Install WSL2 with Ubuntu
   - Install Docker in WSL2
   - Build and run this container
   - Access via RDP or VNC

### For macOS Users

- Use Docker Desktop for Mac
- Build and run this container
- Connect via Microsoft Remote Desktop app (from App Store)

---

## 🎤 Hermes AI Desktop - Quick Start

### Launching Hermes AI Desktop

**Option 1 - Desktop Icon (Recommended):**
1. Connect via RDP to the desktop
2. Open Applications menu
3. Find and click **"Hermes AI Desktop"**
4. First time = Setup wizard appears automatically

**Option 2 - Terminal:**
```bash
hermes
```
Or:
```bash
python3 /opt/hermes-ai/main.py
```

### First-Time Setup (API Key Configuration)

When you first launch Hermes AI Desktop:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✨ Welcome to Hermes AI Desktop                        ║
║                                                           ║
║   To get started, you need an API key:                    ║
║                                                           ║
║   🔑 Get your free API key from:                          ║
║   https://freemodelsforall.hopto.org/                    ║
║                                                           ║
║   Steps:                                                  ║
║   1. Visit the website above                              ║
║   2. Sign up / Log in                                     ║
║   3. Copy your API key                                    ║
║   4. Paste it in the box below                            ║
║                                                           ║
║   ┌─────────────────────────────────────────────────┐     ║
║   │ Paste your API key here...                      │     ║
║   └─────────────────────────────────────────────────┘     ║
║                                                           ║
║   [🚀 Continue with API Key]                              ║
║   [Skip - Use Local Mode Only]                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

**After entering API key:**
- Validates the key automatically
- Saves securely to `~/.hermes/credentials.json`
- Fetches available models
- Opens the chat interface

### Using Hermes AI Desktop

#### Chat Interface

```
┌─────────────────────────────────────────────────────────────┐
│  ✨ Hermes AI                      ⚙️ Settings    │
├──────────────┬──────────────────────────────────────────────┤
│  MODEL       │                                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Claude Opus 5 ▼                                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                       │
│  ➕ New Chat                                          │
│                                                       │
│  CHAT HISTORY                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 💬 Chat                                         │   │
│  │                                                 │   │
│  │ You: Hello!                                     │   │
│  │ ✨ Hello! How can I help you today?             │   │
│  │                                                 │   │
│  │ You: What models are available?                 │   │
│  │ ✨ This gateway supports various models...      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                       │
│  ⚙️ Settings                                          │
│  🔑 API: Configured (sk-abc...)                        │
└──────────────┴──────────────────────────────────────────────┘
```

#### Features

| Feature | Description |
|---------|-------------|
| **Model Selection** | Choose from available AI models via sidebar dropdown |
| **Real-time Chat** | Streaming responses as AI generates text |
| **Tool Integration** | AI can read/write files, list directories |
| **Chat History** | Save and manage multiple conversations |
| **Settings** | Configure API key, view model info |
| **Dark Theme** | Beautiful modern dark UI |

#### Commands

| Action | How To |
|--------|--------|
| Start new chat | Click "➕ New Chat" button |
| Send message | Type in input box + press Enter |
| Change API key | Settings → Change API Key |
| View model info | Settings panel |
| Exit | Close window or use window controls |

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

> ⏱️ **Time**: First build takes 5-15 minutes (includes Python GUI dependencies)

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

### Step 5: Launch Hermes AI Desktop

**From Desktop:**
1. Open Applications menu
2. Find **"Hermes AI Desktop"**
3. Click to launch

**Or from Terminal:**
```bash
hermes
```

**First Time:**
- Welcome screen appears with API key setup
- Visit https://freemodelsforall.hopto.org/ to get API key
- Enter key in the input box
- Click "Continue with API Key"
- Chat interface opens ready to use!

---

## 📁 Files in This Repository

```
ubuntu-xrdp/
├── Dockerfile              # ← Main config (Ubuntu 24.04 + Hermes AI Desktop)
├── hermes-gui/
│   ├── main.py            # ← Hermes AI Desktop application (GUI)
│   └── requirements.txt   # ← Python dependencies
├── start.sh               # Container startup script
├── pulse-client.conf      # Audio config for XRDP
└── README.md              # This file
```

### Which File Does What?

| File | Purpose | Modify For |
|------|---------|------------|
| **Dockerfile** | Base OS, packages, Hermes installation | Change OS, add packages |
| **hermes-gui/main.py** | Hermes AI Desktop GUI application | Customize AI features, UI |
| **hermes-gui/requirements.txt** | Python dependencies | Add/remove Python packages |
| **start.sh** | Service startup | Change service order |
| **pulse-client.conf** | Audio configuration | Audio troubleshooting |

---

## 🛠️ Commands Reference

```bash
# Build the image
docker build -t xrdp .

# Run the container
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp

# Check running containers
docker ps

# View container logs
docker logs xrdp-desktop

# Enter container
docker exec -it xrdp-desktop bash

# Launch Hermes from inside container
docker exec -it xrdp-desktop hermes

# Launch Hermes with query (if supported)
docker exec -it xrdp-desktop bash -c "echo 'your query' | python3 /opt/hermes-ai/main.py"

# Stop container
docker stop xrdp-desktop

# Remove container
docker rm xrdp-desktop

# Full reset (rebuild from scratch)
docker stop xrdp-desktop && docker rm xrdp-desktop && docker rmi xrdp && docker build -t xrdp . && docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

---

## 🔐 Security

### API Key Storage

- API keys are stored in `~/.hermes/credentials.json`
- File permissions set to `600` (only owner can read/write)
- Keys are NEVER logged or shared

### Changing Default Password

```bash
docker build --build-arg ROOT_PASSWORD="YourSecurePassword123!" -t xrdp .
```

---

## 🐛 Troubleshooting

### Hermes Not Found

```bash
# Check if Hermes is installed
which hermes

# If not found, check Python and dependencies
python3 --version
pip3 list | grep customtkinter

# Reinstall if needed
pip3 install customtkinter openai Pillow
```

### Hermes GUI Not Opening

```bash
# Check if tkinter is available
python3 -c "import tkinter; print('tkinter OK')"

# Check for display issues
echo $DISPLAY

# Try running directly
python3 /opt/hermes-ai/main.py
```

### Connection Issues

1. Verify container is running: `docker ps`
2. Check port mapping: `docker port xrdp-desktop`
3. Try: `localhost:3389` or `127.0.0.1:3389`

### Black Screen After Login

1. Check XFCE4: `docker exec xrdp-desktop dpkg -l | grep xfce4`
2. Check session: `docker exec xrdp-desktop cat /root/.xsession`
3. Restart container: `docker restart xrdp-desktop`

### Hermes Shows "API Not Configured"

- First time launch shows setup wizard
- Enter API key from https://freemodelsforall.hopto.org/
- Or configure manually: Settings → Change API Key

---

## 🤝 Contributing

Contributions welcome! When contributing:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test Hermes functionality thoroughly
5. Submit a pull request

---

## 📄 License

Based on [hopingboyz/debianxrdp](https://github.com/hopingboyz/debianxrdp)

Hermes AI Desktop is included as a built-in feature for user assistance.

---

## 🔗 Useful Links

| Resource | Link |
|----------|------|
| Docker Documentation | [docs.docker.com](https://docs.docker.com/) |
| XRDP Project | [github.com/neutrinolabs/xrdp](https://github.com/neutrinolabs/xrdp) |
| XFCE4 Desktop | [xfce.org](https://xfce.org/) |
| Ubuntu Download | [ubuntu.com/download](https://ubuntu.com/download) |
| API Key Portal | [freemodelsforall.hopto.org](https://freemodelsforall.hopto.org/) |
| This Repository | [github.com/jjkh1673-tech/ubuntu-xrdp](https://github.com/jjkh1673-tech/ubuntu-xrdp) |

---

## 🏁 Summary

| Feature | Details |
|---------|---------|
| **Default OS** | Ubuntu 24.04 LTS |
| **Desktop** | XFCE4 |
| **Remote Access** | RDP (port 3389) |
| **AI Desktop** | Hermes AI Desktop (built-in GUI) |
| **AI Gateway** | freemodelsforall.hopto.org |
| **Main Config** | `Dockerfile` |
| **AI Application** | `hermes-gui/main.py` |
| **Quick Build** | `docker build -t xrdp .` |
| **Quick Run** | `docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp` |
| **Launch Hermes** | Click desktop icon OR type `hermes` in terminal |

---

> **💡 TIP**: After connecting via RDP, click the "Hermes AI Desktop" icon in Applications menu. First time it will guide you to get API key from https://freemodelsforall.hopto.org/ - just copy and paste, then you're ready to chat with AI!
