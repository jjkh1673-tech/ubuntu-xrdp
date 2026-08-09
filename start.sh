#!/bin/bash
# ==============================================================================
# XRDP Container Startup Script
# ==============================================================================
# This script initializes the services required for the XRDP remote desktop
# environment when the container starts.
#
# SERVICES STARTED:
#   1. D-Bus: Message bus system (required for desktop environment)
#   2. PulseAudio: Sound server (for audio in remote desktop sessions)
#   3. XRDP: Remote Desktop Protocol server
#
# CUSTOMIZATION NOTES:
#   - This script is generally distribution-agnostic
#   - Service management uses standard init commands
#   - For systemd-based distributions, adjust service commands accordingly
# ==============================================================================

set -e  # Exit on error

echo "=== XRDP Container Starting ==="

# ------------------------------------------------------------------------------
# 1. Start D-Bus service
# ------------------------------------------------------------------------------
# D-Bus is required for inter-process communication in the desktop environment
echo "Starting D-Bus..."
service dbus start

# ------------------------------------------------------------------------------
# 2. Start PulseAudio system server
# ------------------------------------------------------------------------------
# PulseAudio provides audio support for XRDP sessions
# Options:
#   --start:           Start the PulseAudio server
#   --system:          Run as a system-wide instance (not user-specific)
#   --disallow-exit:   Prevent the server from exiting
#   --disable-shm:     Disable shared memory (improves compatibility in containers)
echo "Starting PulseAudio..."
pulseaudio --start --system --disallow-exit --disable-shm

# ------------------------------------------------------------------------------
# 3. Start XRDP service
# ------------------------------------------------------------------------------
# XRDP is the Remote Desktop Protocol server that allows connections
# from RDP clients (Windows Remote Desktop, Remmina, etc.)
echo "Starting XRDP..."
service xrdp start

# ------------------------------------------------------------------------------
# 4. Set up X11 socket directory
# ------------------------------------------------------------------------------
# Create and set permissions on the X11 Unix socket directory
# This is required for X server connections
echo "Setting up X11 socket directory..."
mkdir -p /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

# ------------------------------------------------------------------------------
# 5. Keep container running and monitor XRDP logs
# ------------------------------------------------------------------------------
# Tail the XRDP session manager log to keep the container alive
# and provide visibility into connection attempts and issues
echo "XRDP container ready. Monitoring logs..."
echo "Connect via RDP to: <host-ip>:3389"
echo "Default credentials: root / root (change via ROOT_PASSWORD build arg)"
echo "=== XRDP Container Started ==="

# Follow the XRDP session manager log
tail -f /var/log/xrdp-sesman.log
