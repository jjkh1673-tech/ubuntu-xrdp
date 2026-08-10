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
    libxcb-xinerama0 && \
    apt clean && rm -rf /var/lib/apt/lists/*
# Python3 + pip + tkinter added for Hermes AI Desktop GUI
# libxcb-xinerama0 required for tkinter on some systems

# Install Python dependencies for Hermes GUI
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
# HERMES AI DESKTOP - Built-in AI Agent with Beautiful GUI
# ============================================================================
# Hermes AI Desktop একেবারে বিল্ট-ইন হিসেবে যোগ করা হয়েছে।
# ইউজারকে কোনো অতিরিক্ত সেটআপের প্রয়োজন নেই - ডেস্কটপে আইকনে ক্লিক করুন বা
# টার্মিনালে 'hermes' লিখুন।
# প্রথমবার চালালে API key সেটআপের জন্য উইজার্ড আসবে।
# ============================================================================

# Create Hermes application directory
RUN mkdir -p /opt/hermes-ai

# Copy Hermes application files
COPY hermes-gui/main.py /opt/hermes-ai/main.py
COPY hermes-gui/requirements.txt /opt/hermes-ai/requirements.txt

# Create desktop shortcut for Hermes AI Desktop
RUN mkdir -p /usr/share/applications && \
    mkdir -p /usr/share/icons/hicolor/48x48/apps && \
    mkdir -p /usr/share/icons/hicolor/256x256/apps && \
    echo '[Desktop Entry]
Name=Hermes AI Desktop
Comment=Built-in AI Agent with Beautiful GUI - Ubuntu XRDP
Exec=python3 /opt/hermes-ai/main.py
Icon=hermes-ai
Terminal=false
Type=Application
Categories=Utility;AI;Development;
Keywords=AI;assistant;chatbot;hermes;helper;
StartupNotify=true
StartupWMClass=Hermes' > /usr/share/applications/hermes-ai.desktop

# Create application icon (simple Hermes logo)
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
  <text x="128" y="155" font-family="Arial" font-size="80" font-weight="bold" fill="white" text-anchor="middle">H</text>
</svg>' > /usr/share/icons/hicolor/256x256/apps/hermes-ai.svg && \
    echo '<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
  </defs>
  <circle cx="24" cy="24" r="20" fill="url(#grad)"/>
  <text x="24" y="30" font-family="Arial" font-size="20" font-weight="bold" fill="white" text-anchor="middle">H</text>
</svg>' > /usr/share/icons/hicolor/48x48/apps/hermes-ai.png

# Update icon cache
RUN update-icon-caches /usr/share/icons/hicolor/ 2>/dev/null || true

# Create welcome message that shows on first login
RUN echo '#!/bin/bash
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   ✨ Welcome to Ubuntu XRDP with Hermes AI Desktop        ║"
echo "║                                                           ║"
echo "║   Launch Hermes AI Desktop:                               ║"
echo "║   • Click Hermes AI icon in Applications menu            ║"
echo "║   • Or type in terminal: hermes                          ║"
echo "║                                                           ║"
echo "║   First time? Hermes will guide you to set up API key     ║"
echo "║   for full AI capabilities (required for chat).          ║"
echo "║                                                           ║"
echo "║   API Key Guide: https://freemodelsforall.hopto.org/    ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
' > /etc/profile.d/welcome.sh && chmod +x /etc/profile.d/welcome.sh

# Create terminal launcher script
RUN echo '#!/bin/bash
python3 /opt/hermes-ai/main.py
' > /usr/local/bin/hermes && chmod +x /usr/local/bin/hermes

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

CMD ["/start.sh"]