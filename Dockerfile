# Ubuntu XRDP desktop: Ubuntu 26.04 LTS + XFCE + RDP + the Hermes Agent, in one image.
#
# Everything a person needs after the container starts: a real desktop over RDP, a terminal,
# root through sudo, a fully patched system (no update needed on first boot) and the upstream
# Hermes agent already installed.

FROM ubuntu:26.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
LABEL org.opencontainers.image.title="ubuntu-xrdp" \
      org.opencontainers.image.description="Ubuntu 26.04 LTS desktop (XFCE) over RDP with the Hermes Agent" \
      org.opencontainers.image.licenses="MIT"

# One layer: refresh index, take every pending update, then install the desktop, the everyday
# applications and the development toolchain. Doing the upgrade in the same layer is what makes
# `apt-get upgrade` inside the container report "0 upgraded" right after a fresh start.
RUN apt-get update && \
    apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    xrdp \
    xorgxrdp \
    xorg \
    xfce4 \
    xfce4-goodies \
    xfce4-terminal \
    thunar \
    dbus \
    dbus-x11 \
    dconf-cli \
    zenity \
    libnotify-bin \
    xdg-utils \
    pulseaudio \
    pulseaudio-utils \
    ubuntu-release-upgrader-core \
    update-manager-core \
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
    git \
    curl \
    wget \
    sudo \
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
    mate-calc \
    engrampa \
    ristretto \
    mousepad \
    xfce4-screenshooter \
    xfce4-taskmanager \
    papirus-icon-theme \
    yaru-theme-gtk \
    plank \
    && rm -rf /var/lib/apt/lists/*

# ubuntu:26.04 ships an `ubuntu` user (uid 1000, /bin/bash, sudo group); nothing is created here.
# The xrdp daemon runs as the `xrdp` user and must read the TLS private key, which requires
# membership in the ssl-cert group.
# The account password is 1122 by design - see the README's first-login section for changing it.
RUN usermod -aG ssl-cert xrdp && \
    echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu && \
    echo 'ubuntu:1122' | chpasswd

# Start XFCE (not the xorg-session script shipped by the package) and let anybody open a session.
RUN printf 'startxfce4\n' > /home/ubuntu/.xsession && \
    chown ubuntu:ubuntu /home/ubuntu/.xsession && \
    chmod 700 /home/ubuntu/.xsession && \
    printf 'exec startxfce4\n' > /etc/xrdp/startwm.sh && \
    chmod +x /etc/xrdp/startwm.sh && \
    if [ -f /etc/X11/Xwrapper.config ]; then sed -i 's/^allowed_users=.*/allowed_users=anybody/' /etc/X11/Xwrapper.config; fi

# The real upstream Hermes Agent - installed exactly the way its own documentation says, for the
# ubuntu user, so its home, memory and skills live in the mounted volume and no key is baked in.
# The installer clones the upstream repo anonymously and GitHub throttles bursts of anonymous
# fetches (HTTP 429), so the whole install is retried with a backoff and fails the build loudly if
# every attempt fails.
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

# Hermes Desktop: the same upstream project's own GUI, built by `hermes desktop --build-only`.
# No third-party .deb is installed. If the build cannot run (no network on a custom builder) the
# image is still fine - the launcher then compiles it on first start. The caches are deleted in the
# same layer, because the electron download and the npm cache are ~1 GB of data nothing needs after
# the packaged app exists.
RUN su - ubuntu -c 'export PATH="/home/ubuntu/.local/bin:$PATH"; cd ~ && timeout 1800 hermes desktop --build-only' \
      || echo 'WARNING: Hermes Desktop pre-build did not finish; it will be built on first launch.'; \
    rm -rf /home/ubuntu/.cache/electron /home/ubuntu/.cache/electron-builder \
           /home/ubuntu/.npm /home/ubuntu/.hermes/hermes-agent/node_modules/.cache \
           /var/lib/apt/lists/* /tmp/*

# Desktop look: theme, wallpaper and the left dock.
COPY assets/wallpaper.png /usr/share/backgrounds/wallpaper.png
COPY assets/hermes-ai.png /usr/share/icons/hicolor/256x256/apps/hermes-ai.png
COPY assets/apply-theme.sh /usr/local/bin/apply-theme.sh
COPY assets/apply-theme.desktop /etc/xdg/autostart/apply-theme.desktop
COPY assets/plank.desktop /etc/xdg/autostart/plank.desktop
COPY assets/xfce4-terminal.xml /etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-terminal.xml
RUN chmod +x /usr/local/bin/apply-theme.sh && \
    (gtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true)

# Reference layout keeps only the top panel: strip the default bottom panel (panel-2 + its
# plugins 15-22) from the system default, so fresh sessions never create it.
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

# The desktop apps and launchers: Hermes Desktop, System Upgrade, and the dock items.
COPY assets/hermes-desktop-launch /usr/local/bin/hermes-desktop-launch
COPY assets/ubuntu-migrate /usr/local/bin/ubuntu-migrate
COPY assets/first-run-notice /usr/local/bin/first-run-notice
COPY assets/ubuntu-migrate.desktop /usr/share/applications/ubuntu-migrate.desktop
COPY assets/ubuntu-migrate-notice.desktop /etc/xdg/autostart/ubuntu-migrate-notice.desktop
COPY assets/first-run-notice.desktop /etc/xdg/autostart/first-run-notice.desktop
RUN chmod +x /usr/local/bin/hermes-desktop-launch /usr/local/bin/ubuntu-migrate /usr/local/bin/first-run-notice && \
    printf '%s\n' \
    '[Desktop Entry]' \
    'Name=Hermes Desktop' \
    'Comment=Hermes Agent desktop app (from hermes-agent.nousresearch.com)' \
    'Exec=/usr/local/bin/hermes-desktop-launch' \
    'Icon=/usr/share/icons/hicolor/256x256/apps/hermes-ai.png' \
    'Terminal=false' \
    'Type=Application' \
    'Categories=Development;Utility;' \
    > /usr/share/applications/hermes-ai.desktop

COPY assets/hermes.dockitem /home/ubuntu/.config/plank/dock1/launchers/hermes.dockitem
COPY assets/thunar.dockitem /home/ubuntu/.config/plank/dock1/launchers/thunar.dockitem
COPY assets/xfce4-terminal.dockitem /home/ubuntu/.config/plank/dock1/launchers/xfce4-terminal.dockitem
COPY assets/xfce4-appfinder.dockitem /home/ubuntu/.config/plank/dock1/launchers/xfce4-appfinder.dockitem
COPY assets/ubuntu-migrate.dockitem /home/ubuntu/.config/plank/dock1/launchers/ubuntu-migrate.dockitem

# The Hermes launcher also sits on the desktop (that is where the reference puts it), and the
# shell look is one sourced file so nothing of the distro ~/.bashrc is rewritten.
COPY assets/bash-prompt.sh /etc/skel/.hermes-shell.sh
COPY assets/bash-prompt.sh /home/ubuntu/.hermes-shell.sh
RUN mkdir -p /home/ubuntu/Desktop && \
    cp /usr/share/applications/hermes-ai.desktop /home/ubuntu/Desktop/ && \
    chmod +x /home/ubuntu/Desktop/hermes-ai.desktop && \
    chown -R ubuntu:ubuntu /home/ubuntu/.config /home/ubuntu/Desktop && \
    chown ubuntu:ubuntu /home/ubuntu/.hermes-shell.sh && \
    for f in /home/ubuntu/.bashrc /etc/skel/.bashrc; do \
      grep -q hermes-shell.sh "$f" || printf '\n[ -f ~/.hermes-shell.sh ] && . ~/.hermes-shell.sh\n' >> "$f"; \
    done && \
    chown ubuntu:ubuntu /home/ubuntu/.bashrc

# The image reference the System Upgrade tool prints in its migration plan.
RUN printf '%s\n' 'ubuntu-xrdp:26.04' > /etc/ubuntu-image-ref

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

# xrdp is useless without its session manager, so both must be alive.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD pgrep -x xrdp >/dev/null && pgrep -x xrdp-sesman >/dev/null || exit 1

CMD ["/start.sh"]
