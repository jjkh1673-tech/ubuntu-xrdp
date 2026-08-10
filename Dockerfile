FROM ubuntu:24.04
# Why Ubuntu? Debian Bullseye ছিল মূল বেস, কিন্তু Ubuntu 24.04 LTS বেশি stable,
# বিগিনার ফ্রেন্ডলি, এবং long-term support পায়। এছাড়া Ubuntu-তে প্যাকেজ
# availability বেশি এবং কমিউনিটি সাপোর্ট বেশি।

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
    python3-pip && \
    apt clean && rm -rf /var/lib/apt/lists/*
# Note: firefox-esr ছিল Debian-এর প্যাকেজ, Ubuntu-তে শুধু 'firefox' প্যাকেজ ব্যবহার করা
# হয় যেটি স্বয়ংক্রিয়ভাবে latest stable Firefox দেয়।
# Python3 যোগ করা হয়েছে Hermes AI Agent-এর জন্য।

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
# HERMES AI AGENT - Built-in Intelligent Assistant
# ============================================================================
# Hermes agent একেবারে বিল্ট-ইন হিসেবে যোগ করা হয়েছে।
# ইউজারকে কোনো অতিরিক্ত সেটআপের প্রয়োজন নেই - শুধু 'hermes-agent' লিখলেই চলবে।
# ============================================================================

COPY hermes-agent /usr/local/bin/hermes-agent
RUN chmod +x /usr/local/bin/hermes-agent

# Create desktop shortcut for easy access
RUN mkdir -p /usr/share/applications && \
    echo '[Desktop Entry]
Name=Hermes AI Agent
Comment=Built-in AI assistant for Ubuntu XRDP Desktop
Exec=hermes-agent
Icon=hermes
Terminal=true
Type=Application
Categories=Utility;AI;
Keywords=AI;assistant;chatbot;help;system;
StartupNotify=true' > /usr/share/applications/hermes-agent.desktop

# Create icon directory and simple icon
RUN mkdir -p /usr/share/icons/hicolor/48x48/apps && \
    echo '<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="24" cy="24" r="20" fill="url(#grad)"/>
  <text x="24" y="30" font-family="Arial" font-size="20" fill="white" text-anchor="middle">H</text>
</svg>' > /usr/share/icons/hicolor/48x48/apps/hermes.png

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

CMD ["/start.sh"]