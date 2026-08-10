# Ubuntu XRDP Desktop (built-in ai)

> **Multi-Purpose Linux Environment Deployment with Remote Desktop + Hermes AI Agent & AI Canvas**

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Default-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com)
[![XRDP](https://img.shields.io/badge/XRDP-0.9.x-green.svg)](https://github.com/neutrinolabs/xrdp)
[![AI Canvas](https://img.shields.io/badge/AI_Canvas-Full_GUI_App-purple.svg)](https://github.com/jjkh1673-tech/ubuntu-xrdp)

---

## 🚀 What Is This Project?

This project provides a **Docker container with a full Ubuntu Linux desktop environment** that you can access remotely using Microsoft's Remote Desktop Protocol (RDP). Think of it as a virtual Ubuntu computer that runs inside Docker and can be accessed from Windows, macOS, or another Linux machine.

### 🎤 TWO AI APPLICATIONS INCLUDED

This fork includes **TWO separate AI applications**:

---

## 📱 Application 1: Hermes AI Agent

**Hermes AI Agent** is a **simple terminal-based agent** for:
- Initial setup and API key configuration
- System information queries
- Basic troubleshooting help
- Local mode (no API key needed)

### Features

| Feature | Description |
|---------|-------------|
| **Simple Interface** | Terminal-based, easy to use |
| **Setup Wizard** | Guides API key configuration |
| **System Info** | Query OS, memory, docker info |
| **Local Mode** | Works without API key for basic help |
| **Quick Access** | Type `hermes-agent` in terminal |

### Usage

```bash
# Launch Hermes AI Agent
hermes-agent

# Or from Applications menu
# Click "Hermes AI Agent"
```

### Interface

```
$ hermes-agent

══════════════════════════════════════════════════════════════
  🎤 HERMES AI AGENT - Interactive Mode
  Type 'help' for commands, 'quit' to exit
══════════════════════════════════════════════════════════════

You: help

Hermes: Shows available commands

You: system info

Hermes: Returns system information

You: quit
```

---

## 🎨 Application 2: AI Canvas (Full GUI Application)

**AI Canvas** is the **main full-featured AI desktop application** with complete functionality - a beautiful GUI similar to Claude Desktop.

### Features

✅ **Beautiful Modern GUI**
- Dark theme interface (GitHub-dark inspired)
- Left sidebar with model selection & chat history
- Chat interface with real-time streaming
- Model selection dropdown
- Settings panel
- Professional, polished appearance

✅ **First-Run Setup Wizard**
- Beautiful welcome screen on first launch
- API key input with clear instructions
- Direct link to portal: https://freemodelsforall.hopto.org/
- Step-by-step guidance
- Automatic validation and secure saving

✅ **Complete AI Functionality**
- Real-time streaming chat responses
- Multiple model support via gateway
- Tool integration (file operations)
- Chat history management
- New chat creation
- Model switching on the fly

✅ **Available Tools (Full Functionality)**
| Tool | Description |
|------|-------------|
| `write_file` | Create or overwrite files |
| `delete_file` | Delete files |
| `read_file` | Read file contents |
| `list_directory` | List directory contents |

✅ **Model Support**
- Fetches available models from gateway automatically
- Falls back to hardcoded model list if gateway unavailable
- Default model: Claude Opus 5 (auto-selected)
- Easy model switching via sidebar dropdown

✅ **Error Handling**
- API error detection with retry logic (3 retries)
- Tool compatibility fallback
- Invalid API key detection
- Network error handling
- User-friendly error messages

---

## 🖥️ Interface Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  AI Canvas                                      ⚙️ Settings        │
├──────────────┬───────────────────────────────────────────────────────┤
│              │                                                       │
│  MODEL       │   💬 Chat                                            │
│  ┌──────────│                                                       │
│  │ Claude  │   ┌─────────────────────────────────────────────────┐ │
│  │ Opus 5  │   │                                                 │ │
│  │ ▼       │   │  You: Hello!                                    │ │
│  └─────────│   │  ✨ Hello! How can I help you today?            │ │
│            │   │                                                 │ │
│  CHATS     │   │  You: Create a file test.txt with "Hello"       │ │
│  ┌─────────│   │  ✨ [Thinking with spinner...]                 │ │
│  │ 💬 Chat │   │  ✨ ⚙️ Running tool write_file(...)            │ │
│  │ History │   │  ✨ 📄 Success: File written to 'test.txt'     │ │
│  │         │   │                                                 │ │
│  │ • Chat1 │   │                                                 │ │
│  │ • Chat2 │   └─────────────────────────────────────────────────┘ │
│  │ • New   │                                                      │
│  │   [+]   │   Type your message...                 [Send]        │
│  └─────────│                                                      │
│            │                                                       │
│  +-------------------------------------------------------+       │
│  |  🔑 API: Configured     ⚙️ Settings                   |       │
│  +-------------------------------------------------------+       │
└──────────────────────────────────────────────────────────────────────┘
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

> ⏱️ **Time**: First build takes 5-15 minutes (includes Python GUI dependencies and fonts)

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

### Step 5: Launch Applications

**Option A - From Desktop Menu:**
1. Open Applications menu (start button)
2. Find and click **"AI Canvas"** for full GUI
3. Or click **"Hermes AI Agent"** for simple terminal agent

**Option B - From Terminal:**
```bash
# Launch AI Canvas (full GUI)
ai-canvas

# Or launch Hermes AI Agent (terminal)
hermes-agent
```

### Step 6: First-Time Setup (AI Canvas)

On first launch of AI Canvas:

1. **Welcome screen appears** with API key instructions
2. **Visit**: https://freemodelsforall.hopto.org/
3. **Sign up/Log in** and copy your API key
4. **Paste** the key in the input box
5. **Click** "🚀 Continue with API Key"
6. **Models load** automatically
7. **Start chatting!**

---

## 📁 Files in This Repository

```
ubuntu-xrdp/
├── Dockerfile              # ← Main config (Ubuntu 24.04 + both AI apps)
├── README.md               # ← This file
│
├── hermes-ai/              # ← Hermes AI Agent (simple terminal agent)
│   ├── main.py             # Terminal agent application
│   └── README.md           # Hermes-specific documentation
│
├── ai-canvas/              # ← AI Canvas (full GUI application)
│   ├── main.py             # Main GUI application (full-featured)
│   ├── requirements.txt    # Python dependencies
│   └── icons/
│       └── icon.svg        # Application icon
│
├── hermes-agent            # ← Terminal launcher script (symlink target)
├── start.sh                # Container startup script
└── pulse-client.conf       # Audio config for XRDP
```

### Which File Does What?

| File | Purpose | Modify For |
|------|---------|------------|
| **Dockerfile** | Base OS, packages, app installation | Change OS, add packages |
| **ai-canvas/main.py** | AI Canvas GUI (full features) | Customize GUI, add features |
| **hermes-ai/main.py** | Hermes terminal agent | Customize agent behavior |
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

# Launch AI Canvas from inside container
docker exec -it xrdp-desktop ai-canvas

# Launch Hermes AI Agent from inside container
docker exec -it xrdp-desktop hermes-agent

# Or directly
docker exec -it xrdp-desktop python3 /opt/ai-canvas/main.py
docker exec -it xrdp-desktop python3 /opt/hermes-ai/main.py

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

- **AI Canvas**: Keys stored in `~/.ai_canvas/credentials.json` (permissions 600)
- **Hermes Agent**: Keys stored in `~/.hermes/credentials.json` (permissions 600)
- Keys are NEVER logged or shared
- Environment variables also supported: `API_KEY` or `OPENAI_API_KEY`

### Changing Default Password

```bash
docker build --build-arg ROOT_PASSWORD="YourSecurePassword123!" -t xrdp .
```

---

## 🐛 Troubleshooting

### AI Canvas Not Opening

```bash
# Check if application exists
which ai-canvas
ls -la /opt/ai-canvas/

# Check Python dependencies
pip3 list | grep customtkinter

# Try running directly
python3 /opt/ai-canvas/main.py

# Check for errors
docker exec xrdp-desktop python3 /opt/ai-canvas/main.py 2>&1
```

### Hermes Agent Not Found

```bash
# Check if Hermes is installed
which hermes-agent
ls -la /opt/hermes-ai/

# Reinstall if needed
pip3 install customtkinter openai Pillow
```

### GUI Not Displaying

```bash
# Check if tkinter is available
python3 -c "import tkinter; print('tkinter OK')"

# Check for display issues
echo $DISPLAY

# Check X11 forwarding
docker exec xrdp-desktop echo $DISPLAY
```

### Connection Issues

1. Verify container is running: `docker ps`
2. Check port mapping: `docker port xrdp-desktop`
3. Try: `localhost:3389` or `127.0.0.1:3389`

### Black Screen After Login

1. Check XFCE4: `docker exec xrdp-desktop dpkg -l | grep xfce4`
2. Check session: `docker exec xrdp-desktop cat /root/.xsession`
3. Restart container: `docker restart xrdp-desktop`

### API Key Issues

- First launch shows setup wizard automatically
- Visit https://freemodelsforall.hopto.org/ to get key
- Or configure via Settings panel in AI Canvas

---

## 🤝 Contributing

Contributions welcome! When contributing:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both Hermes and AI Canvas functionality
5. Submit a pull request

---

## 📄 License

Based on [hopingboyz/debianxrdp](https://github.com/hopingboyz/debianxrdp)

Hermes AI Agent and AI Canvas are included as built-in features for user assistance.

---

## 🔗 Useful Links

| Resource | Link |
|----------|------|
| Docker Documentation | [docs.docker.com](https://docs.docker.com/) |
| XRDP Project | [github.com/neutrinolabs/xrdp](https://github.com/neutrinolabs/xrdp) |
| XFCE4 Desktop | [xfce.org](https://xfce.org/) |
| Ubuntu Download | [ubuntu.com/download](https://ubuntu.com/download) |
| **API Key Portal** | **[freemodelsforall.hopto.org](https://freemodelsforall.hopto.org/)** |
| This Repository | [github.com/jjkh1673-tech/ubuntu-xrdp](https://github.com/jjkh1673-tech/ubuntu-xrdp) |

---

## 🏁 Summary

| Feature | Hermes AI Agent | AI Canvas |
|---------|----------------|-----------|
| **Type** | Terminal agent | Full GUI application |
| **Interface** | Command-line | Beautiful desktop GUI |
| **Purpose** | Setup & basic assistance | Full AI chat with tools |
| **API Setup** | Built-in wizard | Built-in wizard |
| **Chat** | Text-based | Streaming GUI chat |
| **Tools** | Basic help | write_file, delete_file, read_file, list_directory |
| **Models** | N/A | Multiple via gateway |
| **Launch** | `hermes-agent` | `ai-canvas` or desktop icon |
| **Complexity** | Simple | Full-featured |

---

## ⚠️ OS Compatibility Notes

| Operating System | Support | Notes |
|------------------|---------|-------|
| **Ubuntu Linux** | ✅ Full Support | Primary target |
| **Debian Linux** | ✅ Full Support | Compatible |
| **Kali Linux** | ⚠️ Experimental | May need adjustments |
| **Windows** | ❌ Apps Not Native | Use RDP to access Linux desktop where apps run |
| **macOS** | ❌ Apps Not Native | Use RDP client to access Linux desktop |

**Important**: Both Hermes AI Agent and AI Canvas are Linux applications designed to run inside the Ubuntu XRDP container. They cannot run directly on Windows or macOS. To use them:
1. Deploy this Docker container
2. Connect via RDP from Windows/macOS
3. Use the applications inside the Linux desktop

---

> **💡 TIP**: After connecting via RDP, you'll see both "AI Canvas" and "Hermes AI Agent" in the Applications menu. Start with AI Canvas for the full experience - it will guide you through API key setup on first launch!
