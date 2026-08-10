# Ubuntu XRDP Desktop (built-in ai)

> **Multi-Purpose Linux Environment Deployment with Remote Desktop + Hermes AI Agent & AI Canvas**

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Default-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com)
[![XRDP](https://img.shields.io/badge/XRDP-0.9.x-green.svg)](https://github.com/neutrinolabs/xrdp)
[![AI Canvas](https://img.shields.io/badge/AI_Canvas-GUI_App-blue.svg)](https://github.com/jjkh1673-tech/ubuntu-xrdp)
[![Hermes AI](https://img.shields.io/badge/Hermes-Agent-Purple.svg)](https://github.com/jjkh1673-tech/ubuntu-xrdp)

---

## 🚀 What Is This Project?

This project provides a **Docker container with a full Ubuntu Linux desktop environment** that you can access remotely using Microsoft's Remote Desktop Protocol (RDP). Inside this container, you get **TWO separate AI applications** with beautiful icons:

1. **🟣 Hermes AI Agent** - Terminal-based agent with purple wings icon
2. **🔵 AI Canvas** - Full GUI application with blue canvas icon

---

## 📌 IMPORTANT: API Key Setup

Both applications use the **SAME API key portal**:

### 🔑 API Key Portal (For BOTH Applications)

**Get your API key from:** **https://freemodelsforall.hopto.org/**

**Instructions:**
1. Visit https://freemodelsforall.hopto.org/
2. Sign up or log in
3. Copy your API key
4. Use this key for either application

---

## 📱 Application 1: 🟣 Hermes AI Agent

### Overview

**Hermes AI Agent** is a **terminal-based AI agent** with:
- ✅ **Purple Wings Icon** - Beautiful icon with Hermes logo (wings + caduceus)
- ✅ **Terminal Mode** - Runs in terminal
- ✅ **API Key via Environment Variable** - Set during deployment
- ✅ **First-Run Prompt** - Or pre-configured via build arg

### Icon

The Hermes AI Agent icon features:
- **Purple gradient background** with wings
- **Gold caduceus symbol** (Hermes' staff with wings)
- **White "H" letter** in center
- **Professional, clean design**

### How to Set API Key for Hermes

**Method 1: Set During Build (Recommended)**

```bash
# Build with API key as build argument
docker build \
  --build-arg HERMES_API_KEY="আপনার-API-কী-এখানে" \
  -t xrdp .
```

**Method 2: Set When Running Container**

```bash
# Run with environment variable
docker run -d -p 3389:3389 \
  -e HERMES_API_KEY="আপনার-API-কী-এখানে" \
  -v xrdp-root-home:/root \
  --name xrdp-desktop \
  xrdp
```

**Method 3: First-Run Prompt (If key not set)**

```bash
# If no API key is set, Hermes will prompt on first run
docker exec -it xrdp-desktop hermes-agent
# Then enter API key when prompted
```

### How to Get API Key

1. Visit: **https://freemodelsforall.hopto.org/**
2. Sign up / Log in
3. Copy your API key
4. Use it in build/run command OR enter when prompted

### Launching Hermes AI Agent

**From Terminal:**
```bash
hermes-agent
```

**From Desktop:**
- Open Applications menu
- Click **"Hermes AI Agent"** icon (purple wings)
- Terminal will open with Hermes running

---

## 🎨 Application 2: 🔵 AI Canvas (Full GUI Application)

### Overview

**AI Canvas** is a **full-featured GUI application** with:
- ✅ **Blue Canvas Icon** - Beautiful icon with paint palette + AI brain
- ✅ **GUI Mode** - Beautiful desktop interface
- ✅ **API Key via Environment Variable** - Set during deployment
- ✅ **First-Run Setup Wizard** - Or pre-configured via build arg

### Icon

The AI Canvas icon features:
- **Dark background** with rounded corners
- **Blue gradient circle** in center
- **Paint palette/drawing canvas** with colorful blocks
- **AI brain symbol** overlay
- **"AI" text** below
- **Modern, attractive design**

### How to Set API Key for AI Canvas

**Method 1: Set During Build**

```bash
# Build with API key
docker build \
  --build-arg HERMES_API_KEY="আপনার-API-কী-এখানে" \
  -t xrdp .
```

**Method 2: Set When Running Container**

```bash
# Run with environment variable
docker run -d -p 3389:3389 \
  -e HERMES_API_KEY="আপনার-API-কী-এখানে" \
  -v xrdp-root-home:/root \
  --name xrdp-desktop \
  xrdp
```

**Method 3: First-Run Wizard (If key not set)**

- Launch AI Canvas from Applications menu or terminal
- Welcome screen appears with API key input
- Enter key and click Continue
- Key saved to `~/.ai_canvas/credentials.json`

### How to Get API Key

1. Visit: **https://freemodelsforall.hopto.org/**
2. Sign up / Log in
3. Copy your API key
4. Use it in build/run command OR enter in first-run wizard

### Launching AI Canvas

**From Terminal:**
```bash
ai-canvas
```

**From Desktop:**
- Open Applications menu
- Click **"AI Canvas"** icon (blue canvas)
- GUI application opens

---

## 🚀 Quick Start (Copy-Paste Guide)

### Step 1: Get API Key

1. Visit **https://freemodelsforall.hopto.org/**
2. Sign up / Log in
3. Copy your API key

### Step 2: Clone This Repository

```bash
git clone https://github.com/jjkh1673-tech/ubuntu-xrdp.git
cd ubuntu-xrdp
```

### Step 3: Build with API Key (Recommended)

```bash
docker build \
  --build-arg HERMES_API_KEY="আপনার-API-কী-এখানে" \
  -t xrdp .
```

> Replace `আপনার-API-কী-এখানে` with your actual API key from https://freemodelsforall.hopto.org/

### Step 4: Run the Container

```bash
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

### Step 5: Connect via RDP

1. Open RDP client
2. Connect to: `localhost:3389`
3. Login: `root` / `root`

### Step 6: Launch Applications

**🟣 Hermes AI Agent (Terminal):**
```bash
hermes-agent
```
Or click purple "Hermes AI Agent" icon in Applications menu

**🔵 AI Canvas (Full GUI):**
```bash
ai-canvas
```
Or click blue "AI Canvas" icon in Applications menu

---

## 📁 Files in This Repository

```
ubuntu-xrdp/
├── Dockerfile              # ← Build configuration (API key support)
├── README.md               # ← This file
│
├── hermes-ai/              # ← Hermes AI Agent (Terminal App)
│   ├── main.py             # Terminal agent code
│   ├── icons/
│   │   ├── hermes-icon.svg              # Vector icon source
│   │   ├── hermes-icon-48x48.png        # 48x48 icon
│   │   ├── hermes-icon-128x128.png      # 128x128 icon
│   │   └── hermes-icon-256x256.png      # 256x256 icon
│   └── README.md           # Hermes documentation
│
├── ai-canvas/              # ← AI Canvas (Full GUI App)
│   ├── main.py             # GUI application code
│   ├── requirements.txt    # Python dependencies
│   └── icons/
│       ├── ai-canvas-icon.svg           # Vector icon source
│       ├── ai-canvas-icon-48x48.png     # 48x48 icon
│       ├── ai-canvas-icon-128x128.png   # 128x128 icon
│       └── ai-canvas-icon-256x256.png   # 256x256 icon
│
├── hermes-agent            # ← Terminal launcher (symlink)
├── start.sh                # Container startup
└── pulse-client.conf       # Audio config
```

---

## 🛠️ Commands Reference

```bash
# Build with API key
docker build --build-arg HERMES_API_KEY="your-key-here" -t xrdp .

# Run with API key
docker run -d -p 3389:3389 -e HERMES_API_KEY="your-key-here" -v xrdp-root-home:/root --name xrdp-desktop xrdp

# Run without API key (will prompt on first launch)
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp

# Launch Hermes AI Agent
hermes-agent

# Launch AI Canvas
ai-canvas

# Enter container
docker exec -it xrdp-desktop bash

# View logs
docker logs xrdp-desktop

# Stop container
docker stop xrdp-desktop

# Full reset
docker stop xrdp-desktop && docker rm xrdp-desktop && docker rmi xrdp && docker build --build-arg HERMES_API_KEY="your-key" -t xrdp . && docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

---

## 🔐 Security

### API Key Storage

| Application | Storage Location | Permissions |
|-------------|------------------|-------------|
| Hermes AI Agent | `~/.hermes/credentials.json` | 600 (owner only) |
| AI Canvas | `~/.ai_canvas/credentials.json` | 600 (owner only) |

### Environment Variables

Both applications support these environment variables:
- `HERMES_API_KEY` - Primary variable (used by both)
- `API_KEY` - Alternative for AI Canvas
- `OPENAI_API_KEY` - Alternative for AI Canvas

### Build-Time Security

- API key passed via `--build-arg` is stored during build
- Key is saved to credentials file with restricted permissions
- To change key: rebuild or use first-run wizard

---

## 🐛 Troubleshooting

### Hermes AI Agent Not Working

```bash
# Check if Hermes is installed
which hermes-agent

# Check if API key is set
cat ~/.hermes/credentials.json

# Launch and check output
hermes-agent
```

### AI Canvas Not Opening

```bash
# Check if AI Canvas is installed
which ai-canvas

# Check Python dependencies
pip3 list | grep customtkinter

# Launch directly
python3 /opt/ai-canvas/main.py
```

### API Key Not Working

```bash
# Check credentials file
cat ~/.hermes/credentials.json
cat ~/.ai_canvas/credentials.json

# Re-enter key via application
hermes-agent  # Will prompt for key
ai-canvas       # Will show setup wizard
```

### Both Applications Use Same Portal

If API key doesn't work:
1. Verify key at https://freemodelsforall.hopto.org/
2. Ensure key is copied correctly (no extra spaces)
3. Try regenerating key if necessary

---

## ⚠️ OS Compatibility Notes

| Operating System | Support | Notes |
|------------------|---------|-------|
| **Ubuntu Linux** | ✅ Full Support | Primary target |
| **Debian** | ✅ Full Support | Compatible |
| **Windows** | ⚠️ Via RDP | Use RDP to access Linux desktop |
| **macOS** | ⚠️ Via RDP | Use RDP client to access Linux desktop |

**Important:** Both Hermes AI Agent and AI Canvas are Linux applications. They run inside the Ubuntu XRDP container. To use them on Windows/macOS:
1. Deploy this Docker container
2. Connect via RDP
3. Use applications inside Linux desktop

---

## 📋 Summary Comparison

| Feature | 🟣 Hermes AI Agent | 🔵 AI Canvas |
|---------|----------------|-----------|
| **Type** | Terminal application | Full GUI application |
| **Interface** | Command-line in terminal | Beautiful desktop GUI |
| **Icon** | Purple wings + H | Blue canvas + AI |
| **API Key Setup** | Build arg OR first-run prompt | Build arg OR first-run wizard |
| **API Key Portal** | https://freemodelsforall.hopto.org/ | https://freemodelsforall.hopto.org/ |
| **Launch Method** | `hermes-agent` or Applications menu | `ai-canvas` or Applications menu |
| **Running Mode** | Terminal | GUI (desktop window) |
| **Primary Use** | Setup & basic assistance | Full AI chat with tools |

---

## 📖 Detailed Instructions

### For 🟣 Hermes AI Agent:

1. **Get API key**: Go to https://freemodelsforall.hopto.org/
2. **Choose setup method**: Build arg OR first-run prompt
3. **If build arg**: `docker build --build-arg HERMES_API_KEY="key" -t xrdp .`
4. **If first-run**: Just run `hermes-agent` and enter key when prompted
5. **Launch**: Type `hermes-agent` or click purple icon in Applications menu
6. **Icon**: Purple wings + caduceus symbol with "H"

### For 🔵 AI Canvas:

1. **Get API key**: Go to https://freemodelsforall.hopto.org/
2. **Choose setup method**: Build arg OR first-run wizard
3. **If build arg**: `docker build --build-arg HERMES_API_KEY="key" -t xrdp .`
4. **If first-run**: Click blue icon, enter key in welcome screen
5. **Launch**: Type `ai-canvas` or click blue icon in Applications menu
6. **Icon**: Blue gradient with paint canvas + AI brain symbol

---

## 🔗 Useful Links

| Resource | Link |
|----------|------|
| Docker Documentation | [docs.docker.com](https://docs.docker.com/) |
| XRDP Project | [github.com/neutrinolabs/xrdp](https://github.com/neutrinolabs/xrdp) |
| Ubuntu Download | [ubuntu.com/download](https://ubuntu.com/download) |
| **API Key Portal (Both Apps)** | **[freemodelsforall.hopto.org](https://freemodelsforall.hopto.org/)** |
| This Repository | [github.com/jjkh1673-tech/ubuntu-xrdp](https://github.com/jjkh1673-tech/ubuntu-xrdp) |

---

> **💡 TIP**: Get your API key from https://freemodelsforall.hopto.org/ first. Then build with `--build-arg HERMES_API_KEY="your-key"` for automatic setup. Both 🟣 Hermes AI Agent and 🔵 AI Canvas will work immediately after deployment!
