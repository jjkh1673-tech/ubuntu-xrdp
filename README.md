# Ubuntu 24.04 XRDP Development Desktop

A clean Ubuntu 24.04 LTS Docker desktop for remote development over XRDP, with the upstream Hermes Agent available from the terminal.

## What is included

- Ubuntu 24.04 LTS
- XFCE desktop over XRDP on TCP 3389
- Python 3 + virtual environments
- Git, OpenSSH client, build-essential and common developer utilities
- Node.js/npm, ripgrep and ffmpeg
- Upstream [Nous Research Hermes Agent](https://github.com/NousResearch/hermes-agent)
- `ai`, `hermes`, `hermes-ai`, and `hermes-agent` commands pointing to the same real Hermes runtime

**AI Canvas is intentionally removed.** It is obsolete and is not part of this project.

## Build

```bash
git clone https://github.com/jjkh1673-tech/ubuntu-xrdp.git
cd ubuntu-xrdp
docker build -t ubuntu-xrdp .
```

No API key is embedded in the Docker image. Configure Hermes after startup with its normal setup flow.

## Run

Choose an RDP password at runtime:

```bash
docker run -d \
  --name ubuntu-xrdp \
  -p 3389:3389 \
  -e XRDP_PASSWORD='choose-a-strong-password' \
  -v ubuntu-xrdp-home:/home/ubuntu \
  ubuntu-xrdp
```

Connect with an RDP client to `<host>:3389` and log in as `ubuntu`.

The `XRDP_PASSWORD` value is applied only when the container starts; it is not stored in the Dockerfile or image layers.

## Hermes Agent

The image installs the real upstream Hermes Agent using the project's official Linux installer. Current upstream documentation recommends:

```bash
hermes
hermes model
hermes setup
hermes doctor
```

`ai`, `hermes-ai`, and `hermes-agent` are compatibility aliases for `hermes`.

On first use, configure a supported provider with `hermes model` or run `hermes setup`. OAuth and other provider credentials remain in the user's Hermes configuration rather than in this repository or Docker build arguments.

## Persistence

Persist `/home/ubuntu` if you want the user's shell configuration and Hermes state to survive container recreation:

```bash
-v ubuntu-xrdp-home:/home/ubuntu
```

## Useful commands

```bash
# Enter the running desktop container
docker exec -it ubuntu-xrdp bash

# Check XRDP processes
docker exec ubuntu-xrdp pgrep -a xrdp

docker exec ubuntu-xrdp pgrep -a xrdp-sesman

# Check Hermes installation
docker exec -it ubuntu-xrdp hermes --help

docker exec -it ubuntu-xrdp hermes doctor

# Restart
docker restart ubuntu-xrdp
```

## Security notes

- Do not commit API keys, OAuth tokens, passwords, `.env` files, or generated credentials.
- Do not use Docker `ARG`/`ENV` to bake model-provider secrets into image layers.
- Set `XRDP_PASSWORD` at runtime and use a strong value.
- Hermes provider credentials should be configured through Hermes' supported authentication/configuration flow.

## Scope

This repository is intentionally focused on a maintainable Ubuntu development workstation: XRDP desktop, developer tooling, and a real Hermes Agent integration. It does not bundle Kali/BlackArch or an unrelated collection of security tools.

## Verification status

Verified on a 4 vCPU / 16 GB GitHub Codespace with Docker 29.7.2:

| Check | Result |
| --- | --- |
| `docker build` | PASS |
| Container starts and stays up | PASS |
| Healthcheck (`xrdp` + `xrdp-sesman`) | PASS - reports `healthy` |
| XRDP listening on TCP 3389 | PASS |
| RDP negotiation + TLS handshake | PASS - `PROTOCOL_SSL`, TLSv1.3, 764-byte certificate |
| XFCE session (headless Xvfb) | PASS - `xfce4-session`, `xfwm4`, `xfce4-panel` |
| `hermes --version` | PASS - Hermes Agent v0.21.1 |
| `ai`, `hermes-ai`, `hermes-agent` | PASS - all resolve to the real Hermes runtime |
| `docker restart` persistence | PASS - returns to `healthy` |
| Secret scan (repository + image layers) | PASS - no credentials found |

Not verified: an interactive login from a real RDP client, and a live model-provider request, which needs the user's own credentials.
