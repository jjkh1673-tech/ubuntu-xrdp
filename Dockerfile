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

# Also save API key for AI Canvas if provided
RUN if [ -n "$HERMES_API_KEY" ]; then \
        mkdir -p /root/.ai_canvas && \
        echo "{\"api_key\": \"$HERMES_API_KEY\", \"saved_at\": \"$(date -Iseconds)\", \"provider\": \"custom_gateway\"}" > /root/.ai_canvas/credentials.json && \
        chmod 600 /root/.ai_canvas/credentials.json && \
        echo "✅ AI Canvas API key pre-configured during build"; \
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

# Copy Hermes icons (REAL LOGO from online)
COPY hermes-ai/icons/hermes-agent-48x48.png /usr/share/icons/hicolor/48x48/apps/hermes-ai.png
COPY hermes-ai/icons/hermes-agent-128x128.png /usr/share/icons/hicolor/128x128/apps/hermes-ai.png
COPY hermes-ai/icons/hermes-agent-256x256.png /usr/share/icons/hicolor/256x256/apps/hermes-ai.png

# Create terminal launcher for Hermes AI
RUN echo '#!/bin/bash\npython3 /opt/hermes-ai/main.py\n' > /usr/local/bin/hermes-agent && chmod +x /usr/local/bin/hermes-agent

# ============================================================================
# AI CANVAS - Full-Featured AI Desktop Application
# ============================================================================

COPY ai-canvas/main.py /opt/ai-canvas/main.py
COPY ai-canvas/requirements.txt /opt/ai-canvas/requirements.txt
COPY ai-canvas/icons/ai-canvas-real-48x48.png /opt/ai-canvas/icons/ai-canvas-icon.png
COPY ai-canvas/icons/ai-canvas-real-128x128.png /usr/share/icons/hicolor/128x128/apps/ai-canvas.png
COPY ai-canvas/icons/ai-canvas-real-256x256.png /usr/share/icons/hicolor/256x256/apps/ai-canvas.png

# Create terminal launchers for AI Canvas
RUN echo '#!/bin/bash\npython3 /opt/ai-canvas/main.py\n' > /usr/local/bin/ai-canvas && chmod +x /usr/local/bin/ai-canvas
RUN echo '#!/bin/bash\npython3 /opt/ai-canvas/main.py\n' > /usr/local/bin/ai && chmod +x /usr/local/bin/ai

RUN chmod +x /opt/ai-canvas/main.py

# Create desktop shortcuts
RUN echo '[Desktop Entry]\nName=AI Canvas\nComment=Full-Featured AI Desktop Application - Chat, Tools, Multiple Models\nExec=ai-canvas\nIcon=ai-canvas\nTerminal=false\nType=Application\nCategories=Utility;AI;Development;Graphics;\nKeywords=AI;assistant;chatbot;canvas;tools;models;\nStartupNotify=true\nStartupWMClass=AI Canvas' > /usr/share/applications/ai-canvas.desktop

RUN echo '[Desktop Entry]\nName=Hermes AI Agent\nComment=Built-in Agent - Setup & Basic Assistant - Terminal Mode\nExec=hermes-agent\nIcon=hermes-ai\nTerminal=true\nType=Application\nCategories=Utility;AI;Development;\nKeywords=AI;agent;setup;helper;terminal;\nStartupNotify=true' > /usr/share/applications/hermes-agent.desktop

# ============================================================================
# WELCOME MESSAGE
# ============================================================================

RUN echo '#!/bin/bash\necho ""\necho "╔════════════════════════════════════════════════════════════════╗"\necho "║                                                                ║"\necho "║   ✨ Welcome to Ubuntu XRDP with AI Applications               ║"\necho "║                                                                ║"\necho "║   Available Applications:                                      ║"\necho "║   • AI Canvas - Full AI Desktop GUI (Applications menu)       ║"\necho "║   • Hermes AI Agent - Terminal Agent (Applications menu)      ║"\necho "║                                                                ║"\necho "║   Terminal Commands:                                           ║"\necho "║   • ai          - Launch AI Canvas GUI (shortcut)             ║"\necho "║   • ai-canvas   - Launch AI Canvas GUI                        ║"\necho "║   • hermes-agent - Launch Hermes terminal agent               ║"\necho "║                                                                ║"\necho "║   ════════════════════════════════════════════════════════════ ║"\necho "║                                                                ║"\necho "║   API KEY INFORMATION:                                         ║"\necho "║   Both applications use the same API key:                     ║"\necho "║   🔑 https://freemodelsforall.hopto.org/                     ║"\necho "║                                                                ║"\necho "║   • Set HERMES_API_KEY during build for auto-configuration    ║"\necho "║     docker build --build-arg HERMES_API_KEY=\"your-key\" -t xrdp ║"\necho "║                                                                ║"\necho "║   • Or set when running:                                       ║"\necho "║     docker run -e HERMES_API_KEY=\"your-key\" ...              ║"\necho "║                                                                ║"\necho "║   • First launch will guide you if key not provided            ║"\necho "║                                                                ║"\necho "╚════════════════════════════════════════════════════════════════╝"\necho ""\n' > /etc/profile.d/welcome.sh && chmod +x /etc/profile.d/welcome.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD service xrdp status || exit 1

CMD ["/start.sh"]
