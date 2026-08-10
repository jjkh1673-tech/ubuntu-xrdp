FROM ubuntu:24.04
# Why Ubuntu 24.04 LTS?
# - stable, beginner-friendly, long-term support
# - better package availability than Debian
# - larger community support

ENV DEBIAN_FRONTEND=noninteractive

# ============================================================================
# API KEY CONFIGURATION (Set during build/deploy time)
# ============================================================================
# Hermes AI Agent এবং AI Canvas উভয়ের জন্যই একই API কী ব্যবহার হয়।
#
# উদাহরণ:
#   docker build --build-arg HERMES_API_KEY="আপনার-API-কী-এখানে" -t xrdp .
#   অথবা
#   docker run -e HERMES_API_KEY="আপনার-API-কী-এখানে" ...
#
# API কী কোথায় পাবেন: https://freemodelsforall.hopto.org/
# ============================================================================

ARG HERMES_API_KEY=""
ENV HERMES_API_KEY=${HERMES_API_KEY}

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

# If HERMES_API_KEY is provided during build, save it to credentials file
RUN if [ -n "$HERMES_API_KEY" ]; then \
        mkdir -p /root/.hermes && \
        echo "{\"api_key\": \"$HERMES_API_KEY\", \"saved_at\": \"$(date -Iseconds)\", \"provider\": \"custom_gateway\"}" > /root/.hermes/credentials.json && \
        chmod 600 /root/.hermes/credentials.json && \
        echo "✅ Hermes API key pre-configured during build"; \
    else \
        echo "⚠️  No HERMES_API_KEY provided during build - Hermes will prompt on first run"; \
    fi

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
    mkdir -p /usr/share/icons/hicolor/128x128/apps && \
    mkdir -p /usr/share/icons/hicolor/256x256/apps

# ============================================================================
# HERMES AI AGENT - Simple Terminal Agent with ICON
# ============================================================================

COPY hermes-agent /opt/hermes-ai/main.py
RUN chmod +x /opt/hermes-ai/main.py

# Copy Hermes icons
COPY hermes-ai/icons/hermes-icon-48x48.png /usr/share/icons/hicolor/48x48/apps/hermes-ai.png
COPY hermes-ai/icons/hermes-icon-128x128.png /usr/share/icons/hicolor/128x128/apps/hermes-ai.png
COPY hermes-ai/icons/hermes-icon-256x256.png /usr/share/icons/hicolor/256x256/apps/hermes-ai.png
RUN ln -sf /usr/share/icons/hicolor/256x256/apps/hermes-ai.png /usr/share/icons/hicolor/48x48/apps/hermes-ai.png

# Create terminal launcher for Hermes AI
RUN echo '#!/bin/bash
python3 /opt/hermes-ai/main.py
' > /usr/local/bin/hermes-agent && chmod +x /usr/local/bin/hermes-agent

# ============================================================================
# AI CANVAS - Full-Featured AI Desktop Application
# ============================================================================

COPY ai-canvas/main.py /opt/ai-canvas/main.py
COPY ai-canvas/requirements.txt /opt/ai-canvas/requirements.txt
COPY ai-canvas/icons/ai-canvas-icon-48x48.png /opt/ai-canvas/icons/ai-canvas-icon.png
COPY ai-canvas/icons/ai-canvas-icon-128x128.png /usr/share/icons/hicolor/128x128/apps/ai-canvas.png
COPY ai-canvas/icons/ai-canvas-icon-256x256.png /usr/share/icons/hicolor/256x256/apps/ai-canvas.png
RUN ln -sf /usr/share/icons/hicolor/256x256/apps/ai-canvas.png /usr/share/icons/hicolor/48x48/apps/ai-canvas.png

RUN chmod +x /opt/ai-canvas/main.py

# Create desktop shortcut for AI Canvas
RUN echo '[Desktop Entry]
Name=AI Canvas
Comment=Full-Featured AI Desktop Application - Chat, Tools, Multiple Models
Exec=ai-canvas
Icon=ai-canvas
Terminal=false
Type=Application
Categories=Utility;AI;Development;Graphics;
Keywords=AI;assistant;chatbot;canvas;tools;models;
StartupNotify=true
StartupWMClass=AI Canvas' > /usr/share/applications/ai-canvas.desktop

# Hermes AI Agent desktop shortcut
RUN echo '[Desktop Entry]
Name=Hermes AI Agent
Comment=Built-in Agent - Setup & Basic Assistant - Terminal Mode
Exec=hermes-agent
Icon=hermes-ai
Terminal=true
Type=Application
Categories=Utility;AI;Development;
Keywords=AI;agent;setup;helper;terminal;
StartupNotify=true' > /usr/share/applications/hermes-agent.desktop

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
echo "║   • AI Canvas - Full AI Desktop GUI (Applications menu)       ║"
echo "║   • Hermes AI Agent - Terminal Agent (Applications menu)      ║"
echo "║                                                                ║"
echo "║   Terminal Commands:                                           ║"
echo "║   • ai-canvas     - Launch AI Canvas GUI                      ║"
echo "║   • hermes-agent  - Launch Hermes terminal agent              ║"
echo "║                                                                ║"
echo "║   ════════════════════════════════════════════════════════════ ║"
echo "║                                                                ║"
echo "║   API KEY INFORMATION:                                         ║"
echo "║   Both applications use the same API key:                     ║"
echo "║   🔑 https://freemodelsforall.hopto.org/                     ║"
echo "║                                                                ║"
echo "║   • Set HERMES_API_KEY during build for auto-configuration    ║"
echo "║     docker build --build-arg HERMES_API_KEY=\"your-key\" -t xrdp ║"
echo "║                                                                ║"
echo "║   • Or set when running:                                       ║"
echo "║     docker run -e HERMES_API_KEY=\"your-key\" ...              ║"
echo "║                                                                ║"
echo "║   • First launch will guide you if key not provided            ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
' > /etc/profile.d/welcome.sh && chmod +x /etc/profile.d/welcome.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

CMD ["/start.sh"]