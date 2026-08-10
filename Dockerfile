FROM ubuntu:24.04
# Why Ubuntu 24.04 LTS?
# - stable, beginner-friendly, long-term support
# - better package availability than Debian
# - larger community support

ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture i386

RUN apt update && apt install -y \
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
    firefox \
    python3 \
    python3-pip \
    python3-urllib3 \
    python3-tk \
    libxcb-xinerama0 \
    libxkbcommon0 \
    libxcb1 \
    libx11-6 \
    libxcb-randr0 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-keysyms1 \
    libxcb-shape0 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-screensaver0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxinerama1 \
    libxrandr2 \
    libxtst6 \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    fonts-wqy-zenhei \
    fonts-arphic-uming \
    fonts-arphic-ukai && \
    apt clean && rm -rf /var/lib/apt/lists/*
# Python3 + pip + tkinter + fonts for GUI applications
# Unicode fonts for proper text rendering

# Install Python dependencies
RUN pip3 install --no-cache-dir customtkinter openai Pillow

# Set root password  
RUN echo "root:root" | chpasswd

RUN sed -i 's/^allowed_users=.*/allowed_users=anybody/' /etc/X11/Xwrapper.config || echo "allowed_users=anybody" >> /etc/X11/Xwrapper.config

RUN echo "startxfce4" > /root/.xsession && chmod 700 /root/.xsession

# Generate machine-id for dbus
RUN mkdir -p /var/run/dbus && dbus-uuidgen > /var/lib/dbus/machine-id

RUN sed -i 's/crypt_level=high/crypt_level=low/' /etc/xrdp/xrdp.ini && \
    sed -i 's/security_layer=negotiate/security_layer=rdp/' /etc/xrdp/xrdp.ini && \
    echo "exec startxfce4" > /etc/xrdp/startwm.sh && chmod +x /etc/xrdp/startwm.sh

RUN adduser xrdp ssl-cert

# ============================================================================
# APPLICATION DIRECTORY STRUCTURE
# ============================================================================

# Create application directories
RUN mkdir -p /opt/hermes-ai && \
    mkdir -p /opt/ai-canvas && \
    mkdir -p /opt/ai-canvas/icons && \
    mkdir -p /usr/share/applications && \
    mkdir -p /usr/share/icons/hicolor/48x48/apps && \
    mkdir -p /usr/share/icons/hicolor/256x256/apps

# ============================================================================
# HERMES AI AGENT - Simple Terminal Agent
# ============================================================================

COPY hermes-agent /opt/hermes-ai/main.py
RUN chmod +x /opt/hermes-ai/main.py

# Create terminal launcher for Hermes AI
RUN echo '#!/bin/bash
python3 /opt/hermes-ai/main.py
' > /usr/local/bin/hermes-agent && chmod +x /usr/local/bin/hermes-agent

# ============================================================================
# AI CANVAS - Full-Featured AI Desktop Application
# ============================================================================

COPY ai-canvas/main.py /opt/ai-canvas/main.py
COPY ai-canvas/requirements.txt /opt/ai-canvas/requirements.txt
COPY ai-canvas/icons/icon.svg /opt/ai-canvas/icons/icon.svg

RUN chmod +x /opt/ai-canvas/main.py

# Create desktop shortcut for AI Canvas
RUN echo '[Desktop Entry]
Name=AI Canvas
Comment=Full-Featured AI Desktop Application - Chat, Tools, Multiple Models
Exec=python3 /opt/ai-canvas/main.py
Icon=ai-canvas
Terminal=false
Type=Application
Categories=Utility;AI;Development;Graphics;
Keywords=AI;assistant;chatbot;canvas;hermes;helper;tools;
StartupNotify=true
StartupWMClass=AI Canvas' > /usr/share/applications/ai-canvas.desktop

# Create desktop shortcut for Hermes AI Agent
RUN echo '[Desktop Entry]
Name=Hermes AI Agent
Comment=Built-in Agent Setup & Basic Assistant - Ubuntu XRDP
Exec=hermes-agent
Icon=hermes-ai
Terminal=true
Type=Application
Categories=Utility;AI;Development;
Keywords=AI;agent;setup;helper;
StartupNotify=true' > /usr/share/applications/hermes-agent.desktop

# ============================================================================
# ICONS
# ============================================================================

# Create AI Canvas icon (SVG for multiple sizes)
RUN echo '<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#58a6ff"/>
      <stop offset="100%" style="stop-color:#3b82f6"/>
    </linearGradient>
  </defs>
  <rect width="256" height="256" rx="40" fill="#0d1117"/>
  <rect width="256" height="256" rx="40" fill="none" stroke="#30363d" stroke-width="2"/>
  <circle cx="128" cy="128" r="80" fill="url(#grad)"/>
  <text x="128" y="155" font-family="Arial, sans-serif" font-size="80" font-weight="bold" fill="white" text-anchor="middle">AI</text>
  <rect x="80" y="180" width="96" height="4" rx="2" fill="#58a6ff" opacity="0.6"/>
</svg>' > /usr/share/icons/hicolor/256x256/apps/ai-canvas.svg && \
    ln -sf /usr/share/icons/hicolor/256x256/apps/ai-canvas.svg /usr/share/icons/hicolor/48x48/apps/ai-canvas.svg

# Create Hermes AI icon
RUN echo '<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
  </defs>
  <rect width="256" height="256" rx="40" fill="#1a1a2e"/>
  <circle cx="128" cy="128" r="80" fill="url(#grad)"/>
  <text x="128" y="155" font-family="Arial, sans-serif" font-size="80" font-weight="bold" fill="white" text-anchor="middle">H</text>
</svg>' > /usr/share/icons/hicolor/256x256/apps/hermes-ai.svg && \
    ln -sf /usr/share/icons/hicolor/256x256/apps/hermes-ai.svg /usr/share/icons/hicolor/48x48/apps/hermes-ai.svg

# Update icon cache
RUN update-icon-caches /usr/share/icons/hicolor/ 2>/dev/null || true

# ============================================================================
# WELCOME MESSAGE
# ============================================================================

RUN echo '#!/bin/bash
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║   ✨ Welcome to Ubuntu XRDP with AI Applications               ║"
echo "║                                                                ║"
echo "║   Available Applications:                                      ║"
echo "║   • AI Canvas - Full AI Desktop (Applications menu)           ║"
echo "║   • Hermes AI Agent - Simple Setup Agent (Applications menu)  ║"
echo "║                                                                ║"
echo "║   Terminal Commands:                                           ║"
echo "║   • ai-canvas     - Launch AI Canvas GUI                      ║"
echo "║   • hermes-agent  - Launch Hermes terminal agent              ║"
echo "║                                                                ║"
echo "║   AI Canvas Setup:                                             ║"
echo "║   First launch will guide you to get API key from:            ║"
echo "║   https://freemodelsforall.hopto.org/                        ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
' > /etc/profile.d/welcome.sh && chmod +x /etc/profile.d/welcome.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

CMD ["/start.sh"]