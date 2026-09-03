# Ubuntu 24.04 XRDP Development Desktop

A clean Ubuntu 24.04 LTS Docker desktop for remote development over XRDP, with the upstream Hermes Agent available from the terminal.

## What is included

- Ubuntu 24.04 LTS
- XFCE desktop over XRDP on TCP 3389
- Python 3 + virtual environments
- Git, OpenSSH client, build-essential and common developer utilities
- Node.js/npm, ripgrep and ffmpeg
- Upstream [Nous Research Hermes Agent](https://github.com/NousResearch/hermes-agent)
- `hermes`, `hermes-ai`, and `hermes-agent` commands pointing to the same real Hermes runtime

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

`hermes-ai` and `hermes-agent` are compatibility aliases for `hermes`.

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

The repository changes can be inspected through GitHub. Docker build, container startup, and an actual RDP client session require a runtime host and are not claimed as verified until they have actually run. The CI build workflow is intended to provide repeatable Docker-build verification.
