FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Refresh the package index, apply every pending Ubuntu update, then install the
# desktop + toolchain, all in one layer so the image ships a fully patched system
# (`apt-get upgrade` inside the container afterwards reports nothing pending).
RUN apt-get update && \
    apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    sudo \
    xrdp \
    xorgxrdp \
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
    python3-dev \
    python3-tk \
    build-essential \
    cmake \
    gdb \
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
    tcpdump \
    nmap \
    procps \
    openssh-client \
    unzip \
    zip \
    jq \
    htop \
    shellcheck \
    papirus-icon-theme \
    yaru-theme-gtk \
    plank \
    x11-apps \
    x11-utils \
    xdotool \
    && rm -rf /var/lib/apt/lists/*

# ubuntu:24.04 already ships an `ubuntu` user (uid 1000, /bin/bash, sudo group).
# The xrdp daemon runs as the `xrdp` user and must read the TLS private key,
# which requires membership in the ssl-cert group.
RUN usermod -aG ssl-cert xrdp && \
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
# The installer clones the upstream repo anonymously and GitHub throttles bursts of anonymous
# fetches (HTTP 429); the installer's own retries span ~35s, which is shorter than GitHub's
# window, so a build could die on a step unrelated to this repository. Retry the whole install
# with a backoff, and fail the build loudly if every attempt fails.
RUN ok=0; \
    for attempt in 1 2 3 4 5; do \
      if su - ubuntu -c 'curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash'; then ok=1; break; fi; \
      echo "Hermes install attempt $attempt failed (GitHub may be rate-limiting this network); retrying in 60s"; \
      sleep 60; \
    done; \
    [ "$ok" = 1 ] || { echo "Hermes Agent install failed after 5 attempts"; exit 1; }; \
    HERMES_BIN="$(find /home/ubuntu/.local/bin /home/ubuntu/.hermes/bin -type f -name hermes -perm -111 -print -quit 2>/dev/null)" && \
    test -n "$HERMES_BIN" && \
    ln -sf "$HERMES_BIN" /usr/local/bin/hermes && \
    ln -sf "$HERMES_BIN" /usr/local/bin/hermes-ai && \
    ln -sf "$HERMES_BIN" /usr/local/bin/hermes-agent && \
    ln -sf "$HERMES_BIN" /usr/local/bin/ai && \
    printf 'export PATH="/home/ubuntu/.local/bin:$PATH"\n' > /etc/profile.d/hermes.sh

# Modern theme, wallpaper and icons.
COPY assets/wallpaper.png /usr/share/backgrounds/wallpaper.png
COPY assets/hermes-ai.png /usr/share/icons/hicolor/256x256/apps/hermes-ai.png
COPY assets/apply-theme.sh /usr/local/bin/apply-theme.sh
COPY assets/apply-theme.desktop /etc/xdg/autostart/apply-theme.desktop
RUN chmod +x /usr/local/bin/apply-theme.sh && \
    (gtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true)

# Reference layout keeps only the top panel: strip the default bottom panel
# (panel-2 + its plugins 15-22) from the system default, so fresh sessions never
# create it. Deleting it at runtime and restarting the panel leaves a zombie
# window, because the running panel keeps a cached panel-2.
RUN python3 - <<'EOF'
import xml.etree.ElementTree as ET
p = '/etc/xdg/xfce4/panel/default.xml'
t = ET.parse(p)
r = t.getroot()
for prop in r.iter('property'):
    if prop.get('name') == 'panels':
        for child in list(prop):
            if child.tag == 'value' and child.get('value') == '2':
                prop.remove(child)
            if child.tag == 'property' and child.get('name') == 'panel-2':
                prop.remove(child)
    if prop.get('name') == 'plugins':
        for child in list(prop):
            n = child.get('name') or ''
            if n.startswith('plugin-'):
                try:
                    i = int(n.split('-')[1])
                except ValueError:
                    continue
                if 15 <= i <= 22:
                    prop.remove(child)
t.write(p, encoding='unicode', xml_declaration=True)
print('panel-2 stripped from default.xml')
EOF

# Hermes Desktop GUI app (Electron). Fork: jjkh1673-tech/hermes-desktop (upstream sir1st/hermes-desktop).
# --retry absorbs the same transient GitHub throttling as the Hermes install above.
RUN curl -fsSL --retry 5 --retry-delay 15 --retry-all-errors -o /tmp/hermes-desktop.deb https://github.com/sir1st/hermes-desktop/releases/download/v0.1.10/Hermes.Desktop-0.1.10-amd64.deb && \
    apt-get update && \
    (dpkg -i /tmp/hermes-desktop.deb || true) && \
    apt-get install -y -f && \
    rm -f /tmp/hermes-desktop.deb && rm -rf /var/lib/apt/lists/*

# Left dock, analog clock widget and Hermes Desktop launcher wiring (reference desktop style).
COPY assets/hermes-desktop-launch /usr/local/bin/hermes-desktop-launch
COPY assets/plank.desktop /etc/xdg/autostart/plank.desktop
COPY assets/hermes.dockitem /home/ubuntu/.config/plank/dock1/launchers/hermes.dockitem
COPY assets/thunar.dockitem /home/ubuntu/.config/plank/dock1/launchers/thunar.dockitem
COPY assets/xfce4-terminal.dockitem /home/ubuntu/.config/plank/dock1/launchers/xfce4-terminal.dockitem
COPY assets/xfce4-appfinder.dockitem /home/ubuntu/.config/plank/dock1/launchers/xfce4-appfinder.dockitem
RUN chmod +x /usr/local/bin/hermes-desktop-launch && \
    chown -R ubuntu:ubuntu /home/ubuntu/.config

RUN mkdir -p /usr/share/applications && \
    printf '%s\n' \
    '[Desktop Entry]' \
    'Name=Hermes Desktop' \
    'Comment=Hermes Desktop app (fork: jjkh1673-tech/hermes-desktop)' \
    'Exec=/usr/local/bin/hermes-desktop-launch' \
    'Icon=/usr/share/icons/hicolor/256x256/apps/hermes-ai.png' \
    'Terminal=false' \
    'Type=Application' \
    'Categories=Development;Utility;' \
    > /usr/share/applications/hermes-ai.desktop

RUN mkdir -p /home/ubuntu/Desktop && \
    cp /usr/share/applications/hermes-ai.desktop /home/ubuntu/Desktop/ && \
    chmod +x /home/ubuntu/Desktop/hermes-ai.desktop && \
    chown -R ubuntu:ubuntu /home/ubuntu/Desktop

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD pgrep -x xrdp >/dev/null && pgrep -x xrdp-sesman >/dev/null || exit 1

CMD ["/start.sh"]
