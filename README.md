# Ubuntu XRDP Desktop in Docker

> **Multi-Purpose Linux Environment Deployment with Remote Desktop**

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Default-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com)
[![XRDP](https://img.shields.io/badge/XRDP-0.9.x-green.svg)](https://github.com/neutrinolabs/xrdp)

---

## What Is This Project?

This project provides a **Docker container with a full Ubuntu Linux desktop environment** that you can access remotely using Microsoft's Remote Desktop Protocol (RDP). Think of it as a virtual Ubuntu computer that runs inside Docker and can be accessed from Windows, macOS, or another Linux machine.

### The Original Project

This repository is a customized version of [hopingboyz/debianxrdp](https://github.com/hopingboyz/debianxrdp), which originally provided an XRDP desktop environment based on **Debian Linux**.

### What Has Been Customized

This fork has been transformed to use **Ubuntu 24.04 LTS** as the default environment:

| Aspect | Original | This Fork |
|--------|----------|-----------|
| **Default Linux** | Debian 11 (Bullseye) | **Ubuntu 24.04 LTS** |
| **Package** | firefox-esr | firefox (Ubuntu standard) |
| **Documentation** | Minimal | Beginner-friendly guide |
| **Supported OS** | Debian-only | Ubuntu, Windows, macOS, Powerful Unix |

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

You should now see the XFCE4 desktop environment!

---

## 🖥️ Supported Operating Systems (2026 Edition)

This project now supports multiple operating systems for different use cases.

### 🐧 Linux Distributions

#### 1. Ubuntu 24.04 LTS (DEFAULT ✅)

| Attribute | Value |
|-----------|-------|
| **Best for** | General use, stability, beginners, AI/ML, development |
| **Compatibility** | ✅ Default - Fully Tested |
| **Why choose it** | Long-term support, huge community, excellent Docker support |
| **Official Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 2. Debian 12 (Bullseye/Bookworm)

| Attribute | Value |
|-----------|-------|
| **Best for** | Server use, minimal setups, stability |
| **Compatibility** | ✅ Compatible - Works with minor changes |
| **Why choose it** | Rock-solid stability, minimal bloat |
| **Official Download** | [debian.org/download](https://www.debian.org/download) |

**How to switch:**
```dockerfile
# Change FROM line in Dockerfile
FROM debian:bullseye
```
Then change `firefox` back to `firefox-esr` in package list.

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

#### 4. Windows 10 (via Docker-OSX or_nested virtualization)

> ⚠️ **Important**: Windows cannot run directly as a Docker container base image.
> Use these options via nested virtualization or VM-in-Docker approaches.

| Attribute | Value |
|-----------|-------|
| **Best for** | Windows application testing, legacy software |
| **Compatibility** | ⚠️ Requires special setup (not native Docker) |
| **Why choose it** | Test Windows apps without dedicated VM |
| **Official ISO** | [microsoft.com/software-download/windows10](https://www.microsoft.com/software-download/windows10) |

**Recommended approach:** Use [docker-windows](https://github.com/jhujx/docker-windows) or run Windows VM alongside Docker.

---

#### 5. Windows 11 (Latest)

| Attribute | Value |
|-----------|-------|
| **Best for** | Latest Windows features, AI-enabled Windows apps |
| **Compatibility** | ⚠️ Requires special setup |
| **Why choose it** | Windows Subsystem for Linux (WSL2) integration |
| **Official ISO** | [microsoft.com/software-download/windows11](https://www.microsoft.com/software-download/windows11) |

---

### 🍎 macOS Options

#### 6. macOS Sonoma (Latest)

> ⚠️ **Important**: macOS cannot run as a Docker base image on non-Apple hardware due to licensing and architecture constraints.

| Attribute | Value |
|-----------|-------|
| **Best for** | iOS/macOS app development, Apple ecosystem testing |
| **Compatibility** | ⚠️ Only on Apple Silicon (M1/M2/M3) hardware |
| **Why choose it** | Test macOS-specific applications |
| **Official** | [apple.com/macos](https://apple.com/macos) |

**Recommended approach:** Use [macos-docker](https://github.com/dockurr/macos) for experimental macOS-in-Docker setups (only on Apple hardware).

---

### ⚡ Powerful Unix Systems for AI & Trending Sectors

#### 7. Alpine Linux (AI/ML Lightweight)

| Attribute | Value |
|-----------|-------|
| **Best for** | Lightweight AI containers, microservices, minimal footprint |
| **Compatibility** | ⚠️ Requires rebuild with apk packages |
| **Why choose it** | Extremely small image size (~5MB base), security-focused |
| **Official** | [alpinelinux.org](https://alpinelinux.org/) |

---

#### 8. Fedora AI (Artificial Intelligence Focus)

| Attribute | Value |
|-----------|-------|
| **Best for** | AI/ML development, PyTorch, TensorFlow, Jupyter |
| **Compatibility** | ⚠️ Requires rebuild |
| **Why choose it** | Fedora has excellent AI/ML tooling, up-to-date packages |
| **Official** | [fedoraproject.org](https://fedoraproject.org/) |

---

#### 9. Rocky Linux / AlmaLinux (Enterprise AI Servers)

| Attribute | Value |
|-----------|-------|
| **Best for** | Enterprise AI deployments, RHEL-compatible environments |
| **Compatibility** | ⚠️ Requires rebuild |
| **Why choose it** | 100% RHEL compatible, stability for production AI workloads |
| **Official** | [rockylinux.org](https://rockylinux.org/) / [almalinux.org](https://almalinux.org/) |

---

#### 10. Arch Linux / Manjaro (Cutting Edge)

| Attribute | Value |
|-----------|-------|
| **Best for** | Latest packages, rolling release, developers who need newest tools |
| **Compatibility** | ⚠️ Requires pacman-based rewrite |
| **Why choose it** | Always latest software, AUR access |
| **Official** | [archlinux.org](https://archlinux.org/) / [manjaro.org](https://manjaro.org/) |

---

#### 11. NixOS (Reproducible AI Environments)

| Attribute | Value |
|-----------|-------|
| **Best for** | Reproducible AI/ML environments, declarative configuration |
| **Compatibility** | ⚠️ Requires rewrite |
| **Why choose it** | Reproducible builds, isolated environments, functional package management |
| **Official** | [nixos.org](https://nixos.org/) |

---

#### 12. OpenSUSE (AI Development)

| Attribute | Value |
|-----------|-------|
| **Best for** | AI development, containers, SUSE ecosystem |
| **Compatibility** | ⚠️ Requires rebuild |
| **Why choose it** | Good container support, YaST configuration, stable |
| **Official** | [opensuse.org](https://www.opensuse.org/) |

---

## 📊 Quick Comparison Table

| OS | Docker Base | AI/ML Ready | Beginner Friendly | Status |
|----|-------------|-------------|-------------------|--------|
| **Ubuntu 24.04 LTS** | ✅ Yes | ✅ Excellent | ✅ Yes | **DEFAULT** |
| Debian 12 | ✅ Yes | ✅ Good | ⚠️ Moderate | Compatible |
| Kali Linux | ✅ Yes | ⚠️ Tools only | ⚠️ Learning curve | Experimental |
| Windows 10/11 | ❌ No (VM needed) | ⚠️ Via WSL2 | ✅ Yes | Special setup |
| macOS | ❌ No (Apple only) | ✅ Good | ✅ Yes | Apple hardware only |
| Alpine Linux | ✅ Yes | ⚠️ Lightweight | ⚠️ Advanced | Requires rebuild |
| Fedora | ✅ Yes | ✅ Excellent | ⚠️ Moderate | Requires rebuild |
| Rocky/AlmaLinux | ✅ Yes | ✅ Enterprise | ⚠️ Server-focused | Requires rebuild |
| Arch/Manjaro | ⚠️ Community | ✅ Cutting-edge | ⚠️ Rolling release | Requires rewrite |
| NixOS | ⚠️ Experimental | ✅ Reproducible | ⚠️ Unique paradigm | Requires rewrite |

---

## 🔐 Security Notes

1. **Default password is `root`** - Change it for production use
2. **Windows/macOS** require separate licensing and cannot run as Docker base images
3. **Kali Linux** is for authorized security testing only

---

## 📁 Files in This Repository

```
ubuntu-xrdp/
├── Dockerfile        # ← Main config (Ubuntu 24.04 by default)
├── start.sh          # Container startup script
├── pulse-client.conf # Audio config for XRDP
└── README.md         # This file
```

---

## 🛠️ Commands

```bash
# Build
docker build -t xrdp .

# Run
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp

# Stop
docker stop xrdp-desktop

# Logs
docker logs xrdp-desktop
```

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📄 License

Based on [hopingboyz/debianxrdp](https://github.com/hopingboyz/debianxrdp)