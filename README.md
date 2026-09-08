# Ubuntu 24.04 XRDP Development Desktop

An Ubuntu 24.04 LTS Docker container with a graphical XFCE desktop over RDP, developer
tooling, and the upstream Hermes AI agent in the terminal.

## Prerequisites

Docker, installed and running. Check:

```bash
docker --version
docker info >/dev/null && echo "Docker is working"
```

If the second line errors, start Docker Desktop (Windows/macOS) or run
`sudo systemctl start docker` (Linux), then check again.

You also need about 7 GB of free disk space.

## Quick start

Run these one at a time.

**1. Build** (roughly 8 minutes the first time):

```bash
git clone https://github.com/jjkh1673-tech/ubuntu-xrdp.git
cd ubuntu-xrdp
docker build -t ubuntu-xrdp .
```

**2. Start.** Replace `choose-a-strong-password` with your own. Skipping this is the most
common mistake: without it you cannot log in.

```bash
docker run -d \
  --name ubuntu-xrdp \
  -p 3389:3389 \
  -e XRDP_PASSWORD='choose-a-strong-password' \
  -v ubuntu-xrdp-home:/home/ubuntu \
  ubuntu-xrdp
```

**3. Wait ~30 seconds**, then check:

```bash
docker inspect --format '{{.State.Health.Status}}' ubuntu-xrdp
```

Wait until it prints `healthy`. The desktop takes a few seconds to come up.

**4. Connect** with any RDP client:

| Where Docker runs | Address |
| --- | --- |
| Your own computer | `localhost:3389` |
| Another machine | `<that machine's IP>:3389` |

Username `ubuntu`, password from step 2.

Clients: Remmina (Linux), Remote Desktop Connection (Windows), Microsoft Remote Desktop
(macOS).

The container uses a self-signed certificate, so the client warns on first connect. That
is expected — accept it.

## Using the AI agent

Open a terminal in the desktop, or run `docker exec -it ubuntu-xrdp bash`, then:

```bash
ai
```

`ai`, `hermes`, `hermes-ai` and `hermes-agent` all launch the same real Hermes agent.

On first run no provider is configured. Set one up:

```bash
hermes setup
```

Credentials go to `~/.hermes/.env` with `600` permissions. They are never written into the
image, and `hermes status` displays them masked.

## What is included

- Ubuntu 24.04 LTS with an XFCE desktop over XRDP on TCP 3389
- Python 3 with pip, venv and development headers
- C/C++ via build-essential and cmake, with gdb for debugging
- Node.js and npm
- Git, OpenSSH client, ripgrep, jq, shellcheck, htop
- Network and security tools: net-tools, iproute2, dnsutils, tcpdump, nmap
- ffmpeg
- Upstream [Nous Research Hermes Agent](https://github.com/NousResearch/hermes-agent)

**AI Canvas is intentionally removed.** It is obsolete and is not part of this project.

Data-science and ML libraries are deliberately left to `pip` inside a virtualenv, so the
image stays maintainable:

```bash
python3 -m venv ~/venv && source ~/venv/bin/activate
pip install numpy pandas scikit-learn
```

## Persistence

The `-v ubuntu-xrdp-home:/home/ubuntu` volume in step 2 keeps your shell configuration and
Hermes credentials when the container is recreated. Without it they survive
`docker restart` but are lost if you remove the container.

## Useful commands

```bash
docker exec -it ubuntu-xrdp bash          # shell inside the container
docker exec ubuntu-xrdp pgrep -a xrdp     # is XRDP running?
docker logs ubuntu-xrdp                   # startup log
docker restart ubuntu-xrdp                # restart
docker stop ubuntu-xrdp                   # stop
docker rm -f ubuntu-xrdp                  # remove (volume is kept)
```

## Troubleshooting

**Cannot log in over RDP.** `XRDP_PASSWORD` is applied only when the container starts. If
it was missing, the log shows:

```text
WARNING: XRDP_PASSWORD is not set; the ubuntu account cannot be used for password login.
```

Recreate the container with `-e XRDP_PASSWORD=...`. Changing it on a running container
does nothing.

**Status is `starting`, not `healthy`.** Normal for the first ~30 seconds. If it stays
`unhealthy`:

```bash
docker logs ubuntu-xrdp
docker exec ubuntu-xrdp pgrep -a xrdp
docker exec ubuntu-xrdp pgrep -a xrdp-sesman
```

Both `xrdp` and `xrdp-sesman` must be running for the healthcheck to pass.

**Connection refused on 3389.** Confirm the port is published with `docker ps`, then:

```bash
docker exec ubuntu-xrdp ss -ltn
```

**Black or frozen desktop on first login.** Close the client and reconnect; the first
session initialises the XFCE profile and can take a few seconds.

**Hermes says no provider is configured.** Expected on a fresh container. Run
`hermes setup`.

## Known limitations

- The TLS certificate is self-signed, so RDP clients warn on first connect.
- The image is around 6 GB; it bundles a desktop environment and a full build toolchain.
- No GPU acceleration. CUDA workloads need extra configuration.
- The `gh` CLI is not bundled, because it requires a third-party apt repository. Install
  it on demand if you need it.
- Hermes configuration lives in `/home/ubuntu`; see Persistence.

## Security notes

- Do not commit API keys, OAuth tokens, passwords or `.env` files.
- Do not use Docker `ARG`/`ENV` to bake provider secrets into image layers.
- Set `XRDP_PASSWORD` at runtime and use a strong value.
- Configure Hermes providers through `hermes setup`, not through build arguments.

## Scope

A maintainable Ubuntu development workstation: XRDP desktop, developer tooling, and a real
Hermes integration. It does not bundle Kali/BlackArch or bulk security tooling.

## Verification status

Verified on a 4 vCPU / 16 GB GitHub Codespace with Docker 29.7.2.

| Check | Result |
| --- | --- |
| `docker build --no-cache` | PASS |
| GitHub Actions CI build | PASS |
| Container starts and stays up | PASS |
| Healthcheck (`xrdp` + `xrdp-sesman`) | PASS - reports `healthy` |
| XRDP listening on TCP 3389 | PASS |
| RDP negotiation + TLS handshake | PASS - `PROTOCOL_SSL`, TLSv1.3 |
| Real RDP client session (`xfreerdp`) | see below |
| XFCE session (headless Xvfb) | PASS - `xfce4-session`, `xfwm4`, `xfce4-panel` |
| `ai`, `hermes`, `hermes-ai`, `hermes-agent` | PASS - all launch the real runtime |
| `hermes --version` | PASS - Hermes Agent v0.21.1 |
| First-run detection (`hermes status`, `hermes doctor`) | PASS |
| Secret masking | PASS - masked in output, absent from logs and image layers |
| Persistence across container recreation (volume) | PASS |
| `docker restart` | PASS - returns to `healthy` |
| Secret scan (repository + image layers) | PASS - no credentials found |

Not verified: a live model-provider request, which needs your own credentials.
