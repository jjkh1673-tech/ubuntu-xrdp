FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    sudo \
    xrdp \
    xfce4 \
    xfce4-goodies \
    xorg \
    dbus-x11 \
    dbus \
    pulseaudio \
    pulseaudio-utils \
    python3 \
    python3-pip \
    python3-venv \
    python3-tk \
    build-essential \
    nodejs \
    npm \
    ripgrep \
    ffmpeg \
    nano \
    vim \
    less \
    net-tools \
    iproute2 \
    dnsutils \
    procps \
    openssh-client \
    unzip \
    zip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ubuntu && \
    usermod -aG sudo,ssl-cert ubuntu && \
    echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu

# Configure XFCE for XRDP and allow Xorg sessions.
RUN printf 'startxfce4\n' > /home/ubuntu/.xsession && \
    chown ubuntu:ubuntu /home/ubuntu/.xsession && \
    chmod 700 /home/ubuntu/.xsession && \
    printf 'exec startxfce4\n' > /etc/xrdp/startwm.sh && \
    chmod +x /etc/xrdp/startwm.sh && \
    sed -i 's/^allowed_users=.*/allowed_users=anybody/' /etc/X11/Xwrapper.config || true

# Install the real upstream Hermes Agent. No custom wrapper and no API key is baked into the image.
RUN su - ubuntu -c 'curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash' && \
    HERMES_BIN="$(find /home/ubuntu/.local/bin /home/ubuntu/.hermes/bin -type f -name hermes -perm -111 -print -quit 2>/dev/null)" && \
    test -n "$HERMES_BIN" && \
    ln -sf "$HERMES_BIN" /usr/local/bin/hermes && \
    ln -sf "$HERMES_BIN" /usr/local/bin/hermes-ai && \
    ln -sf "$HERMES_BIN" /usr/local/bin/hermes-agent && \
    printf 'export PATH="/home/ubuntu/.local/bin:$PATH"\n' > /etc/profile.d/hermes.sh

RUN mkdir -p /usr/share/applications && \
    printf '%s\n' \
    '[Desktop Entry]' \
    'Name=Hermes AI' \
    'Comment=Upstream Hermes Agent terminal' \
    'Exec=xfce4-terminal -e hermes' \
    'Terminal=false' \
    'Type=Application' \
    'Categories=Development;Utility;' \
    > /usr/share/applications/hermes-ai.desktop

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD pgrep -x xrdp >/dev/null && pgrep -x xrdp-sesman >/dev/null || exit 1

CMD ["/start.sh"]
