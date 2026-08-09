# Linux XRDP Desktop in Docker

> **Multi-Purpose Linux Environment Deployment with Remote Desktop**

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Default-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com)
[![XRDP](https://img.shields.io/badge/XRDP-0.9.x-green.svg)](https://github.com/neutrinolabs/xrdp)

---

## What Is This Project?

This project provides a **Docker container with a full Linux desktop environment** that you can access remotely using Microsoft's Remote Desktop Protocol (RDP). Think of it as a virtual Linux computer that runs inside Docker and can be accessed from Windows, macOS, or another Linux machine.

### The Original Project

This repository is a customized version of [hopingboyz/debianxrdp](https://github.com/hopingboyz/debianxrdp), which originally provided an XRDP desktop environment based on **Debian Linux**.

### What Has Been Customized

This fork has been transformed into a **multi-purpose Linux environment deployment project**:

| Aspect | Original | This Fork |
|--------|----------|-----------|
| **Default Linux** | Debian 11 (Bullseye) | **Ubuntu 24.04 LTS** |
| **Documentation** | Minimal | Comprehensive beginner-friendly guide |
| **Distribution Support** | Debian-only | Ubuntu (default), Debian, Kali documented |
| **Customization** | Hard to modify | Clear customization points |
| **Security** | Hard-coded password | Password via build argument |

---

## Quick Start (Copy-Paste Guide)

### Prerequisites

Before you begin, make sure you have:

- ✅ **Docker installed** on your system
- ✅ **Terminal/command prompt** access
- ✅ **RDP client** (Windows Remote Desktop, Remmina for Linux, or Microsoft Remote Desktop for macOS)

### Step 1: Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/debianxrdp.git
cd debianxrdp
```

Replace `YOUR_USERNAME` with your GitHub username if you forked it, or use the original URL.

### Step 2: Build the Docker Image

```bash
docker build -t xrdp .
```

This command:
- Reads the `Dockerfile`
- Downloads Ubuntu 24.04 LTS as the base
- Installs all required software (XRDP, XFCE4 desktop, Wine, Firefox, etc.)
- Creates a Docker image named `xrdp`

> ⏱️ **Time**: First build takes 3-10 minutes depending on your internet speed.

### Step 3: Run the Container

```bash
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

This command:
- `-d`: Runs in background (detached mode)
- `-p 3389:3389`: Maps port 3389 (RDP) from container to your computer
- `-v xrdp-root-home:/root`: Creates a persistent volume for root's home directory
- `--name xrdp-desktop`: Names the container for easy reference

### Step 4: Connect via RDP

1. Open your RDP client
2. Connect to: `localhost:3389` (or your machine's IP address)
3. Login with:
   - **Username**: `root`
   - **Password**: `root` (or the password you set)

You should now see the XFCE4 desktop environment!

---

## 🎯 Linux Environment Selection Guide

This section helps you choose the right Linux distribution for your needs.

### How to Select Your Environment

The Linux distribution is controlled by the **`FROM` line in the Dockerfile**:

```dockerfile
# === CUSTOMIZATION POINT: Select Your Linux Distribution ===
# Uncomment and modify the line below to change the base image
# FROM ubuntu:24.04    # DEFAULT - Ubuntu 24.04 LTS
# FROM debian:bullseye # Alternative - Debian 11
# FROM kalilinux/kali-rolling  # Alternative - Kali Linux
# ================================================
FROM ubuntu:24.04
# ============================================================
```

> **📍 FILE TO EDIT**: `Dockerfile` (line ~20)
>
> **📖 README SECTION**: See distribution-specific instructions below

---

### Sector-Based Distribution Recommendations

#### 1. General Linux / Beginner

**Recommended**: Ubuntu 24.04 LTS

| Attribute | Value |
|-----------|-------|
| **Best for** | Beginners, general use, stability |
| **Compatibility** | ✅ Default - Tested |
| **Why choose it** | Easy to use, large community, long-term support |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |
| **Documentation** | [ubuntu.com/docs](https://ubuntu.com/docs) |

---

#### 2. Defensive Security / Blue Team

**Recommended**: Ubuntu 24.04 LTS or Debian 12

| Attribute | Value |
|-----------|-------|
| **Best for** | Security monitoring, log analysis, defensive tools |
| **Compatibility** | ✅ Tested (Ubuntu) / ✅ Compatible (Debian) |
| **Why choose it** | Stable, secure, well-documented |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 3. Offensive Security / Authorized Security Testing

> ⚠️ **WARNING**: Only use these environments on systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal.

**Recommended**: Kali Linux

| Attribute | Value |
|-----------|-------|
| **Best for** | Penetration testing, security audits, CTF challenges |
| **Compatibility** | ⚠️ Experimental - Requires testing |
| **Why choose it** | Pre-installed security tools, active development |
| **ISO Download** | [kali.org/get-kali](https://www.kali.org/get-kali/) |
| **Documentation** | [kali.org/docs](https://www.kali.org/docs/) |

**File to edit**: `Dockerfile`
```dockerfile
FROM kalilinux/kali-rolling
```

**What changes**: Package installation may need adjustment for Kali-specific package names.

**Do NOT change**: The overall XRDP/XFCE4 setup remains the same.

---

#### 4. Penetration Testing / Security Research

**Recommended**: Kali Linux or BlackArch Linux

| Attribute | Value |
|-----------|-------|
| **Best for** | Advanced security research, exploit development |
| **Compatibility** | ⚠️ Kali: Experimental / ⚠️ BlackArch: Not currently compatible |
| **Why choose it** | Comprehensive security tool collections |
| **ISO Download (Kali)** | [kali.org/get-kali](https://www.kali.org/get-kali/) |
| **ISO Download (BlackArch)** | [blackarch.org](https://blackarch.org/) |

---

#### 5. Digital Forensics

**Recommended**: Ubuntu 24.04 LTS with forensic tools

| Attribute | Value |
|-----------|-------|
| **Best for** | Forensic analysis, evidence examination |
| **Compatibility** | ✅ Tested |
| **Why choose it** | Stable environment for forensic tools |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 6. Privacy / Security Research

**Recommended**: Ubuntu 24.04 LTS or Tails (for live USB)

| Attribute | Value |
|-----------|-------|
| **Best for** | Privacy-focused work, anonymous browsing |
| **Compatibility** | ✅ Ubuntu: Tested / ⚠️ Tails: Not applicable (live USB only) |
| **Why choose it** | Good balance of privacy and usability |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 7. Programming / Software Development

**Recommended**: Ubuntu 24.04 LTS

| Attribute | Value |
|-----------|-------|
| **Best for** | General development, Python, web development |
| **Compatibility** | ✅ Default - Tested |
| **Why choose it** | Great package availability, widely used by developers |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 8. Automation

**Recommended**: Ubuntu 24.04 LTS

| Attribute | Value |
|-----------|-------|
| **Best for** | Scripting, task automation, CI/CD |
| **Compatibility** | ✅ Tested |
| **Why choose it** | Stable, reliable, extensive tooling |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 9. Data Science

**Recommended**: Ubuntu 24.04 LTS

| Attribute | Value |
|-----------|-------|
| **Best for** | Data analysis, Jupyter notebooks, ML development |
| **Compatibility** | ✅ Tested |
| **Why choose it** | Excellent Python/R support, large ecosystem |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 10. AI / Machine Learning

**Recommended**: Ubuntu 24.04 LTS

| Attribute | Value |
|-----------|-------|
| **Best for** | ML model development, GPU computing |
| **Compatibility** | ✅ Tested |
| **Why choose it** | CUDA support, PyTorch/TensorFlow compatibility |
| **ISO Download** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 11. Cybersecurity Learning Lab

**Recommended**: Kali Linux or Ubuntu 24.04 LTS

| Attribute | Value |
|-----------|-------|
| **Best for** | Learning cybersecurity, practicing in isolated labs |
| **Compatibility** | ⚠️ Kali: Experimental / ✅ Ubuntu: Tested |
| **Why choose it** | Kali: tools pre-installed / Ubuntu: stability for learning |
| **ISO Download (Kali)** | [kali.org/get-kali](https://www.kali.org/get-kali/) |
| **ISO Download (Ubuntu)** | [ubuntu.com/download](https://ubuntu.com/download) |

---

#### 12. General Server / DevOps

**Recommended**: Ubuntu 24.04 LTS Server

| Attribute | Value |
|-----------|-------|
| **Best for** | Server deployments, DevOps tooling |
| **Compatibility** | ✅ Tested |
| **Why choose it** | LTS support, widely adopted in server environments |
| **ISO Download** | [ubuntu.com/download/server](https://ubuntu.com/download/server) |

---

## 📋 Linux Distribution Reference Table

| # | Distribution | Primary Purpose | Recommended For | Status | Official Link |
|---|--------------|----------------|-----------------|--------|---------------|
| 1 | **Ubuntu 24.04 LTS** | General purpose, stability | Beginners, developers, servers | ✅ **DEFAULT** | [ubuntu.com](https://ubuntu.com/download) |
| 2 | **Debian 12** | Stability, server use | Advanced users, servers | ✅ Compatible | [debian.org](https://www.debian.org/download) |
| 3 | **Kali Linux** | Security testing | Authorized penetration testers | ⚠️ Experimental | [kali.org](https://www.kali.org/get-kali/) |
| 4 | **BlackArch** | Security research | Advanced security researchers | ❌ Not Compatible | [blackarch.org](https://blackarch.org/) |
| 5 | **Linux Mint** | Beginner-friendly desktop | Windows migrants, beginners | 📝 Documented | [linuxmint.com](https://linuxmint.com/download.php) |
| 6 | **Fedora Workstation** | Latest technologies | Developers, enthusiasts | 📝 Documented | [fedoraproject.org](https://fedoraproject.org/workstation/download) |
| 7 | **openSUSE** | System administration | Sysadmins, developers | 📝 Documented | [opensuse.org](https://www.opensuse.org/download/) |
| 8 | **Pop!_OS** | Gaming, productivity | Gamers, content creators | 📝 Documented | [pop.system76.com](https://pop.system76.com/) |
| 9 | **Manjaro** | User-friendly Arch | Arch users who want ease | 📝 Documented | [manjaro.org](https://manjaro.org/download/) |
| 10 | **Arch Linux** | Customization, learning | Advanced users | ❌ Requires rewrite | [archlinux.org](https://archlinux.org/download/) |
| 11 | **Alpine Linux** | Minimal, containers | Advanced container users | ❌ Requires rewrite | [alpinelinux.org](https://alpinelinux.org/downloads/) |
| 12 | **Tails** | Privacy, anonymity | Privacy-focused users | ❌ Not applicable | [tails.net](https://tails.net/install/) |
| 13 | **Parrot OS** | Security, privacy | Security enthusiasts | ⚠️ Experimental | [parrotlinux.org](https://parrotlinux.org/download/) |
| 14 | **elementary OS** | Beautiful desktop | Design-conscious users | 📝 Documented | [elementary.io](https://elementary.io/download) |
| 15 | **Zorin OS** | Windows-like experience | Windows migrants | 📝 Documented | [zorin.com](https://zorin.com/os/download/) |

---

## 🔧 How to Switch Linux Distributions

### Ubuntu (Default) → Debian

1. Open `Dockerfile`
2. Find the `FROM` line
3. Change:
   ```dockerfile
   FROM ubuntu:24.04
   ```
   To:
   ```dockerfile
   FROM debian:bullseye
   ```
4. Rebuild: `docker build -t xrdp-debian .`
5. Run: `docker run -d -p 3389:3389 --name xrdp-debian -v xrdp-root-home:/root xrdp-debian`

### Ubuntu (Default) → Kali Linux

> ⚠️ **EXPERIMENTAL**: Kali support is documented but not fully tested.

1. Open `Dockerfile`
2. Change:
   ```dockerfile
   FROM ubuntu:24.04
   ```
   To:
   ```dockerfile
   FROM kalilinux/kali-rolling
   ```
3. You may need to adjust package names (Kali uses different package versions)
4. Rebuild and test

> **Note**: Kali Linux is intended for authorized security testing only.

### Ubuntu (Default) → BlackArch Linux

> ❌ **NOT CURRENTLY COMPATIBLE**

BlackArch uses the `pacman` package manager, which requires a complete rewrite of the package installation section. This distribution is documented for reference but is not currently supported by this repository's architecture.

---

## 📦 Understanding ISO Images vs. Container Base Images

> **⚠️ IMPORTANT DISTINCTION**

This project uses **Docker container base images**, NOT bootable ISO files. Here's the difference:

### Linux ISO (Installation Image)

- Used to **install Linux** on a physical computer or virtual machine
- Contains a complete Linux system installer
- Examples: Ubuntu Desktop ISO, Kali Linux ISO
- Downloaded from distribution websites
- **Not directly usable as a Docker base image**

### Docker Base Image

- A **minimal pre-configured system** used as a starting point for containers
- Optimized for running specific services
- Examples: `ubuntu:24.04`, `debian:bullseye`, `python:3.11`
- Referenced in Dockerfile with `FROM` directive
- Downloaded automatically by Docker from Docker Hub

### What This Means for You

When you see a distribution listed in this README with an ISO download link, that ISO is **NOT** what this project uses. Instead, this project uses the official Docker image for that distribution (when available).

| Distribution | Has Docker Image? | Can Be Used Here? |
|--------------|-------------------|-------------------|
| Ubuntu | ✅ Yes (`ubuntu:24.04`) | ✅ Default |
| Debian | ✅ Yes (`debian:bullseye`) | ✅ Compatible |
| Kali Linux | ✅ Yes (`kalilinux/kali-rolling`) | ⚠️ Experimental |
| BlackArch | ❌ No official Docker image | ❌ Not compatible |
| Arch Linux | ❌ No official Docker image | ❌ Not compatible |
| Alpine | ✅ Yes (`alpine:latest`) | ❌ Requires rewrite |

---

## 🔐 Security Considerations

### Default Password

The default password is set via a build argument:

```bash
# Default (NOT recommended for production)
docker build -t xrdp .

# Custom password (RECOMMENDED)
docker build --build-arg ROOT_PASSWORD="YourSecurePassword123!" -t xrdp .
```

### Security Best Practices

1. **Never use default credentials in production**
2. **Change the password** using the `ROOT_PASSWORD` build argument
3. **Use a non-root user** for enhanced security (advanced)
4. **Keep the container updated** by rebuilding periodically
5. **Only expose port 3389** to trusted networks

### For Security Testing Environments

If you're using Kali Linux or similar distributions for security testing:

- ✅ Only test on systems you own or have explicit permission to test
- ✅ Use isolated lab environments for practice
- ✅ Follow responsible disclosure practices
- ❌ Never use for unauthorized access to computer systems

---

## 📁 Repository Structure

```
debianxrdp/
│
├── Dockerfile              # ← MAIN CONFIGURATION FILE
│                           #   Controls: base OS image, packages, system setup
│                           #   EDIT THIS to change Linux distribution
│
├── start.sh                # Container startup script
│                           #   Starts: D-Bus, PulseAudio, XRDP
│                           #   Generally doesn't need modification
│
├── pulse-client.conf       # PulseAudio client configuration
│                           #   Enables audio in XRDP sessions
│                           #   Distribution-agnostic
│
└── README.md               # ← YOU ARE HERE
                                Comprehensive documentation
```

### Which File Controls What?

| File | Controls | Change For Distribution Switch? |
|------|----------|--------------------------------|
| **Dockerfile** | Base OS image, packages, system configuration | ✅ **YES - Primary file** |
| start.sh | Service startup order, container behavior | ❌ Usually no |
| pulse-client.conf | Audio configuration | ❌ No |
| README.md | Documentation only | ❌ No |

---

## 🛠 Advanced Customization

### Adding More Packages

Edit the `Dockerfile` and add packages to the `apt-get install` line:

```dockerfile
RUN apt-get update && apt-get install -y \
    xrdp \
    xfce4 \
    xfce4-goodies \
    # ... existing packages ...
    your-package-here \    # ← Add new packages here
    && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### Changing the Desktop Environment

The default desktop is XFCE4. To use a different desktop:

1. Install the desktop environment package
2. Update the `.xsession` file
3. Update `/etc/xrdp/startwm.sh`

Example for LXDE:

```dockerfile
# Install LXDE
RUN apt-get install -y lxde

# Set LXDE as default session
RUN echo "startlxde" > /root/.xsession
RUN echo "exec startlxde" > /etc/xrdp/startwm.sh
```

### Customizing XFCE4

XFCE4 settings can be customized by adding configuration files or modifying the startup sequence.

---

## 🐛 Troubleshooting

### Build Issues

**Problem**: `docker build` fails with "no space left on device"

**Solution**: Clean up Docker resources
```bash
docker system prune -a
```

**Problem**: Package installation fails

**Solution**: Check that the distribution's package repository is accessible. For Ubuntu, ensure you're using a valid release.

### Connection Issues

**Problem**: Cannot connect via RDP

**Solution**:
1. Verify the container is running: `docker ps`
2. Check port mapping: `docker port xrdp-desktop`
3. Ensure port 3389 is not blocked by firewall
4. Try connecting to `localhost:3389` or `127.0.0.1:3389`

**Problem**: "Connection refused"

**Solution**:
1. Check XRDP logs: `docker logs xrdp-desktop`
2. Verify XRDP service started: `docker exec xrdp-desktop service xrdp status`
3. Ensure no other service is using port 3389

### Login Issues

**Problem**: Authentication fails

**Solution**:
1. Verify credentials: default is `root` / `root`
2. Check if password was customized during build
3. Try uppercase/lowercase variations

**Problem**: Black screen after login

**Solution**:
1. Check XFCE4 is installed: `docker exec xrdp-desktop dpkg -l | grep xfce4`
2. Verify `.xsession` exists: `docker exec xrdp-desktop cat /root/.xsession`
3. Check XRDP configuration: `docker exec xrdp-desktop cat /etc/xrdp/startwm.sh`

### Audio Issues

**Problem**: No sound in RDP session

**Solution**:
1. Verify PulseAudio is running: `docker exec xrdp-desktop pulseaudio --check`
2. Check PulseAudio logs: `docker exec xrdp-desktop journalctl -u pulseaudio`
3. Ensure RDP client supports audio redirection

### Performance Issues

**Problem**: Slow or laggy desktop

**Solution**:
1. Increase Docker resource allocation (CPU, memory)
2. Use a lighter desktop environment (LXDE instead of XFCE4)
3. Check network latency to the container host
4. Try disabling visual effects in XFCE4

---

## 🔄 Returning to Default Ubuntu Configuration

If you've made changes and want to return to the default Ubuntu configuration:

```bash
# Reset to default Ubuntu Dockerfile
git checkout Dockerfile

# Or manually edit Dockerfile to use:
# FROM ubuntu:24.04

# Rebuild
docker build -t xrdp .
```

---

## 📊 What Gets Installed

The default Ubuntu configuration includes:

| Component | Purpose |
|-----------|---------|
| **XRDP** | Remote Desktop Protocol server |
| **XFCE4** | Lightweight desktop environment |
| **XFCE4 Goodies** | Additional XFCE4 plugins and themes |
| **Xorg** | X Window System server |
| **D-Bus** | Inter-process communication |
| **PulseAudio** | Sound server for audio |
| **Wine** | Windows application compatibility |
| **Wine32** | 32-bit Windows application support |
| **Firefox** | Web browser |
| **sudo** | Privilege escalation |
| **curl/wget** | Network utilities |
| **nano** | Text editor |
| **net-tools** | Network diagnostics |

---

## 🔄 Updating the Container

To update the container with new packages or changes:

```bash
# Stop and remove old container
docker stop xrdp-desktop
docker rm xrdp-desktop

# Rebuild image (if you made changes)
docker build -t xrdp .

# Start new container
docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp
```

---

## 📝 Commands Reference

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

# Stop the container
docker stop xrdp-desktop

# Start the container
docker start xrdp-desktop

# Remove the container
docker rm xrdp-desktop

# Remove the image
docker rmi xrdp

# Execute commands inside the container
docker exec -it xrdp-desktop bash

# View XRDP logs inside container
docker exec xrdp-desktop tail -f /var/log/xrdp-sesman.log
```

---

## 🤝 Contributing

Contributions are welcome! When contributing:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

Please ensure:
- Documentation is updated for any configuration changes
- Ubuntu remains the default configuration
- Security best practices are maintained

---

## 📄 License

This project is based on the original work by hopingboyz. See the original repository for license information.

---

## 🔗 Useful Links

| Resource | Link |
|----------|------|
| Docker Documentation | [docs.docker.com](https://docs.docker.com/) |
| XRDP Project | [github.com/neutrinolabs/xrdp](https://github.com/neutrinolabs/xrdp) |
| XFCE4 Desktop | [xfce.org](https://xfce.org/) |
| Ubuntu Download | [ubuntu.com/download](https://ubuntu.com/download) |
| Kali Linux | [kali.org](https://www.kali.org/) |
| BlackArch Linux | [blackarch.org](https://blackarch.org/) |
| Wine (Windows compatibility) | [winehq.org](https://www.winehq.org/) |

---

## 🏁 Summary

| Topic | Details |
|-------|---------|
| **Default Linux** | Ubuntu 24.04 LTS |
| **Desktop Environment** | XFCE4 |
| **Remote Access** | RDP (port 3389) |
| **Main Config File** | `Dockerfile` (change `FROM` line) |
| **Quick Build** | `docker build -t xrdp .` |
| **Quick Run** | `docker run -d -p 3389:3389 -v xrdp-root-home:/root --name xrdp-desktop xrdp` |
| **Default Login** | root / root (change with ROOT_PASSWORD build arg) |

---

> **💡 TIP**: Bookmark this README for easy reference when customizing your Linux environment!
