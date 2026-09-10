# Ubuntu XRDP desktop (XFCE) with the Hermes Agent

A Docker image of a complete Ubuntu 26.04 LTS desktop that you open with any RDP client. It is
not a demo: after the container starts you get a normal XFCE desktop, a terminal, root through
`sudo`, everyday applications, and the upstream [Hermes Agent](https://hermes-agent.nousresearch.com)
already installed. The system is patched during the build, so you never have to run an update
before working, and a `System Upgrade` tool tells you when a newer Ubuntu LTS exists and moves you
to it without touching your files.

Who it is for: someone who wants a Linux desktop and a coding environment on any machine (Windows,
macOS, Chromebook, an old laptop) without installing Linux on it, and who wants an AI agent that can
actually run commands in that desktop.

## Desktop preview

What a user sees after connecting over RDP, captured in a real `xfreerdp` session logged in as
`ubuntu` (1280x800, first login, nothing hand-edited afterwards):

![Ubuntu XRDP desktop: classic dark wallpaper, single top panel, left Plank dock with Hermes Desktop, Files, terminal, app finder and System Upgrade, Hermes Desktop icon on the desktop](assets/preview.png)

## What is inside

| Part | Detail |
| --- | --- |
| Base | Ubuntu 26.04 LTS (resolute), every update applied at build time |
| Desktop | XFCE 4.20 over xrdp 0.10, single top panel, left dock (Plank) |
| User | `ubuntu` (uid 1000), passwordless `sudo`, RDP login |
| Terminals & editors | xfce4-terminal (dark palette, 10k scrollback), mousepad, `vim`, `nano` |
| Everyday apps | Thunar (files), mousepad (text editor), ristretto (images), engrampa (archives), mate-calc, xfce4-screenshooter, xfce4-taskmanager, htop |
| Development | git, curl, wget, jq, python3 (+venv/pip/tk), nodejs, npm, build-essential, cmake, gdb, ripgrep, shellcheck, openssh-client, nmap, tcpdump, dnsutils |
| AI | Hermes Agent installed by its own installer, plus `ai`, `hermes`, `hermes-agent`, `hermes-ai` commands and the `hermes desktop` GUI |
| Upgrades | `ubuntu-migrate` command, a `System Upgrade` entry in the menu and dock, and a login notice when a newer Ubuntu LTS exists |
| Ports | 3389/tcp (RDP) |

Nothing is faked or stubbed: no wrapper scripts pretending to be the agent, no half-configured
services. `docker exec` in and everything behaves like the upstream tool.

## Requirements

- Docker installed and running (`docker --version` and `docker info >/dev/null && echo ok`).
- About 15 GB free disk (the finished image is roughly 12 GB) and 4 GB of RAM for the desktop.
- An RDP client: `Remmina` or `mstsc` (Windows), `Microsoft Remote Desktop` (macOS), `xfreerdp` (Linux).

## Run it

```bash
git clone https://github.com/jjkh1673-tech/ubuntu-xrdp.git
cd ubuntu-xrdp
docker build -t ubuntu-xrdp .
docker run -d --name ubuntu-xrdp -p 3389:3389 \
  -v ubuntu-xrdp-home:/home/ubuntu \
  ubuntu-xrdp
docker logs -f ubuntu-xrdp      # stop with Ctrl-C once it says the desktop is ready
```

Then point an RDP client at `localhost` (port 3389) and log in:

```
user: ubuntu
password: 1122
```

The `-v ubuntu-xrdp-home:/home/ubuntu` part is what keeps your files, shell history and Hermes
memory when you delete and recreate the container. Add it always.

### Publishing the image (optional)

CI only builds the image; nothing is pushed to a registry, because creating the package needs a
token with `write:packages`, which a workflow token does not get on a personal account. If you want
your own image in GHCR, tag and push it once:

```bash
echo <token with write:packages> | docker login ghcr.io -u <you> --password-stdin
docker tag ubuntu-xrdp:26.04 ghcr.io/<you>/ubuntu-xrdp:latest && docker push ghcr.io/<you>/ubuntu-xrdp:latest
```

### First login: change the password

The image ships with the documented default password `1122` so that a personal machine or your own
codespace just works. On anything reachable from outside, change it before you connect anything else:

```bash
docker exec -it ubuntu-xrdp su - ubuntu -c 'passwd'        # inside the container
# or set your own at start-up:
docker run -d --name ubuntu-xrdp -p 3389:3389 -e XRDP_PASSWORD='Y0uRs3cret!' ubuntu-xrdp
# or from inside the desktop: open a terminal and run  passwd
```

The first login also shows a welcome bubble with the same reminder.

### Connecting from another machine

Replace `localhost` with the host's address. Same credentials. If you expose 3389 to the internet,
change the password first and consider a VPN or an SSH tunnel:

```bash
ssh -N -L 3389:localhost:3389 you@that-host      # then connect to localhost:3389
```

### Using a GitHub Codespace instead of your own machine

1. In this repository open **Codepaces → New codespace** (the default 4 vCPU / 16 GB machine is
   what this image was built and verified on).
2. In the codespace terminal run the two `docker` commands from *Run it* above.
3. Open the **Ports** tab, find `3389`, and set *Port visibility* to **Public** if you want to reach
   it from another machine without a tunnel. Codespace ports are forwarded over HTTPS, so an RDP
   client must go through a tunnel instead:
   ```bash
   gh codespace ssh -c <codespace-name> -- -L 3389:localhost:3389
   ```
   then connect an RDP client to `localhost:3389`.
4. Your codespace is private to you even though this repository is public; nothing is shared with
   anyone else unless you hand out the address and the password.

## Root

The `ubuntu` user has full root with no password:

```bash
sudo -i        # uid=0(root)
```

Use it for packages, services and system files. It is deliberate, because the whole desktop is
already isolated in a container.

## Hermes in the terminal

The agent is installed the way its documentation says, for the `ubuntu` user, from
`https://hermes-agent.nousresearch.com/install.sh`. Its home is `~/.hermes` - inside the volume, so
it survives rebuilds.

```bash
ai                # or: hermes
hermes setup      # first run: pick a provider, paste the API key
hermes status
hermes doctor
```

No API key is baked into the image, and no wrapper replaces the real CLI - `ai` and `hermes` are the
same binary, so every upstream command and capability is available.

## Hermes Desktop

`hermes desktop` is the upstream app for this agent, so that is what is used here - it is compiled
into the image at build time and launched by:

- the **Hermes Desktop** icon on the desktop,
- the **Hermes** icon in the left dock,
- the `Hermes Desktop` entry in the Applications menu,
- `/usr/local/bin/hermes-desktop-launch` from a terminal.

It shares the same `~/.hermes` state as the terminal, so a chat you started in the terminal is where
you left it in the app. If you build a custom image without network access, the pre-build is
skipped with a warning and the first launch compiles it (a few minutes, once).

## Staying up to date

The image is fully patched at build time, so right after a fresh start there is nothing to install:

```bash
sudo apt-get update -qq && apt-get -s upgrade | tail -1     # 0 upgraded
```

For the desktop itself there is `ubuntu-migrate` (the **System Upgrade** icon in the dock and menu):

```bash
ubuntu-migrate --check              # current Ubuntu, newest LTS, exit code says if a move is due
ubuntu-migrate --plan               # the exact docker commands that swap the image, keeping the volume
ubuntu-migrate --apply              # refresh packages inside the running container (root)
ubuntu-migrate --migrate-lts        # Ubuntu's own do-release-upgrade, if you prefer in-place
ubuntu-migrate notifications off    # stop the login notice; 'on' turns it back
```

Once per release you get a notification when a newer LTS exists. It never installs anything on its
own. Because your `/home/ubuntu` is a volume, `--plan` is the safe path: pull the new image, recreate
the container, and every file, setting and Hermes state comes with you unchanged.

## Repository layout

```
Dockerfile                  the image: Ubuntu 26.04 + XFCE + xrdp + tooling + Hermes
start.sh                    container entrypoint: dbus, audio, xrdp, then tails the RDP log
assets/apply-theme.sh       per-login session look (theme, icons, wallpaper, dock position)
assets/*.desktop            autostart entries: theme, plank, welcome notice, upgrade notice
assets/*.dockitem           what the left dock pins
assets/xfce4-terminal.xml   terminal colours, font and scrollback defaults
assets/ubuntu-migrate       the System Upgrade tool
assets/hermes-desktop-launch  launches `hermes desktop`
assets/wallpaper.png        the desktop background
.github/workflows/ci.yml    builds the image on every push
```

## Customising

- Wallpaper: replace `assets/wallpaper.png` and rebuild; the session script points at it.
- Dock: edit the `assets/*.dockitem` files - one line each, pointing at a `.desktop` file.
- More packages: add them to the `apt-get install` list in the Dockerfile.
- No clock widget: the desktop is deliberately plain; the panel keeps the stock XFCE clock.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| RDP client says the certificate is untrusted | Expected: xrdp generates a self-signed certificate. Accept it or pass `/cert:ignore` to `xfreerdp`. |
| Login window appears and immediately disconnects | Wrong password, or the volume's `/home/ubuntu` is not writable: `docker logs ubuntu-xrdp`. |
| Black screen after login | Delete the session: `docker exec ubuntu-xrdp rm -f /home/ubuntu/.xsession-errors` then reconnect; if it repeats, `docker restart ubuntu-xrdp`. |
| `xrdp: already running` after a restart | The entrypoint removes the stale pid files; if you replaced `start.sh`, keep `rm -f /var/run/xrdp/*.pid`. |
| No sound | Audio redirection is best-effort; check `/var/log/pulseaudio.log` inside the container. |
| Want a fresh desktop | `docker rm -f ubuntu-xrdp && docker volume rm ubuntu-xrdp-home` then run again. |

## Verified

Measured on a GitHub Codespace of this repository (`standardLinux32gb`: 4 vCPU, 16 GB RAM, root
through passwordless sudo), Docker 29.7.2, after `docker system prune -af` so the build started from
an empty image store. The RDP checks were done by driving a real `xfreerdp` client against the
container and typing the credentials into the login window.

<!--VERIFY-->

## Notes

- The image is MIT-licensed like the desktop it installs; Hermes Agent is upstream (Nous Research)
  and is fetched by its own installer at build time, so the agent you get is the one upstream ships.
- No API key, token or password other than the documented default is stored in the image.
- Firefox and Chrome are snap packages on Ubuntu and snapd cannot run inside this container, so a
  browser is not preinstalled; `xdg-open` and the Hermes browsing tools still work with any browser
  you install from a `.deb`.
