# ==============================================================================
# Linux Environment Deployment - XRDP Desktop in Docker
# ==============================================================================
# DEFAULT ENVIRONMENT: Ubuntu 24.04 LTS
# ==============================================================================
# This Dockerfile creates a Docker container with XRDP remote desktop,
# XFCE4 desktop environment, Wine for Windows application support,
# and Firefox ESR web browser.
#
# SUPPORTED LINUX ENVIRONMENTS:
#   - Ubuntu 24.04 LTS (DEFAULT - tested)
#   - Debian 12 (Bullseye/Bookworm) - compatible
#   - Kali Linux - documented alternative
#   - BlackArch Linux - experimental
#
# For distribution-specific instructions, see README.md
# ==============================================================================

# ==============================================================================
# CUSTOMIZATION POINT: Change the base image to select a different distribution
# ==============================================================================
# Ubuntu (DEFAULT - recommended for most users):
FROM ubuntu:24.04
# ^^^^^^^^
# DEFAULT: Ubuntu 24.04 LTS - stable, beginner-friendly, well-supported

# --- ALTERNATIVE DISTRIBUTIONS (uncomment and adjust as needed) ---
#
# Debian 12 (Bullseye):
# FROM debian:bullseye
# ^^^^^^^^
# COMPATIBLE: Works with minimal changes. apt package manager is same.
# NOTE: Some package names may differ (e.g., firefox-esr vs firefox)
#
# Kali Linux (rolling):
# FROM kalilinux/kali-rolling
# ^^^^^^^^
# EXPERIMENTAL: Requires testing. Kali-specific packages may be needed.
# WARNING: Kali is for authorized security testing only.
#
# BlackArch Linux:
# NOT CURRENTLY COMPATIBLE - requires major redesign for pacman-based system
# ^^^^^^^^
# EXPERIMENTAL: Would need complete package list rewrite for pacman.
# Documented for reference only.
# ==============================================================================

# ==============================================================================
# Environment configuration
# ==============================================================================
# NONINTERACTIVE: Prevents apt prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Optional: Customize root password via build argument (defaults to 'root')
# For production, ALWAYS set this to a secure value
# Usage: docker build --build-arg ROOT_PASSWORD="YourSecurePassword" -t xrdp .
ARG ROOT_PASSWORD=root

# ==============================================================================
# System preparation
# ==============================================================================
# Add i386 architecture for Wine 32-bit support
RUN dpkg --add-architecture i386

# ==============================================================================
# Package installation
# ==============================================================================
# INSTALLED COMPONENTS:
#   - xrdp: Remote Desktop Protocol server
#   - xfce4 + xfce4-goodies: Lightweight desktop environment
#   - xorg: X Window System
#   - dbus-x11: D-Bus session bus for X11
#   - sudo: Privilege escalation
#   - curl, wget: Network utilities
#   - nano: Text editor
#   - net-tools: Network diagnostics (ifconfig, netstat)
#   - policykit-1: Policy kit for authentication
#   - pulseaudio + pulseaudio-utils: Audio server
#   - wine + wine32: Windows application compatibility layer
#   - firefox: Web browser
#
# NOTE: Package names are compatible across Debian/Ubuntu.
#       For Kali, some packages may have different names.
# ==============================================================================
RUN apt-get update && apt-get install -y \
    xrdp \
    xfce4 \
    xfce4-goodies \
    xorg \
    dbus-x11 \
    sudo \
    curl \
    wget \
    nano \
    net-tools \
    policykit-1 \
    pulseaudio \
    pulseaudio-utils \
    wine \
    wine32 \
    firefox && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ==============================================================================
# User configuration
# ==============================================================================
# Set root password from build argument
# SECURITY NOTE: For production deployments, use Docker secrets or
#               environment variables instead of hardcoding passwords.
#               Consider using non-root users for enhanced security.
RUN echo "root:${ROOT_PASSWORD}" | chpasswd

# ==============================================================================
# X11 configuration for XRDP
# ==============================================================================
# Allow any user to start X server (required for XRDP)
RUN sed -i 's/^allowed_users=.*/allowed_users=anybody/' /etc/X11/Xwrapper.config || \
    echo "allowed_users=anybody" >> /etc/X11/Xwrapper.config

# Set XFCE4 as the default session
RUN echo "startxfce4" > /root/.xsession && \
    chmod 700 /root/.xsession

# ==============================================================================
# D-Bus initialization
# ==============================================================================
# Generate machine-id for D-Bus (required for proper service operation)
RUN mkdir -p /var/run/dbus && \
    dbus-uuidgen > /var/lib/dbus/machine-id

# ==============================================================================
# XRDP configuration
# ==============================================================================
# Configure XRDP for compatibility:
#   - Lower crypt_level for broader client compatibility
#   - Use RDP security layer (more compatible than negotiate)
#   - Set XFCE4 as the window manager
RUN sed -i 's/crypt_level=high/crypt_level=low/' /etc/xrdp/xrdp.ini && \
    sed -i 's/security_layer=negotiate/security_layer=rdp/' /etc/xrdp/xrdp.ini && \
    echo "exec startxfce4" > /etc/xrdp/startwm.sh && \
    chmod +x /etc/xrdp/startwm.sh

# Add xrdp user to ssl-cert group (required for certificate access)
RUN adduser xrdp ssl-cert || true

# ==============================================================================
# Copy initialization scripts
# ==============================================================================
# start.sh: Main container startup script
# pulse-client.conf: PulseAudio client configuration for XRDP audio
COPY start.sh /start.sh
COPY pulse-client.conf /etc/pulse/client.conf

RUN chmod +x /start.sh

# ==============================================================================
# Network configuration
# ==============================================================================
# Expose RDP port (default RDP port)
EXPOSE 3389

# ==============================================================================
# Container startup
# ==============================================================================
# Start the XRDP service and related processes
CMD ["/start.sh"]
