#!/bin/bash
# Applies a modern theme + wallpaper once the XFCE session is up.
sleep 4
xfconf-query -c xsettings -p /Net/ThemeName     -t string -s "Yaru-dark"    --create 2>/dev/null
xfconf-query -c xsettings -p /Net/IconThemeName -t string -s "Papirus-Dark" --create 2>/dev/null
MON=$(xrandr --listmonitors 2>/dev/null | awk 'NR==2{print $NF}')
for m in "$MON" 0 Virtual1 rdp0; do
  [ -z "$m" ] && continue
  P="/backdrop/screen0/monitor$m/workspace0"
  xfconf-query -c xfce4-desktop -p "$P/last-image"  -t string -s /usr/share/backgrounds/wallpaper.png --create 2>/dev/null
  xfconf-query -c xfce4-desktop -p "$P/image-style" -t int    -s 5 --create 2>/dev/null
  xfconf-query -c xfce4-desktop -p "$P/color-style" -t int    -s 0 --create 2>/dev/null
done
xfdesktop --reload 2>/dev/null
# Reference-desktop style: dock on the left (plank reads gsettings/dconf).
gsettings set "net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/" position left 2>/dev/null
# Upgraders with an old profile may still have panel-2 in their own config
# (fresh installs never get it: it is stripped from default.xml at build time).
# Delete it, then fully restart the panel so it re-reads the config.
# NOTE: plain `xfce4-panel -r` reuses the cached panel-2 and leaves a zombie
# window; quit + start is required.
if xfconf-query -c xfce4-panel -p /panels/panel-2 >/dev/null 2>&1; then
  xfconf-query -c xfce4-panel -p /panels/panel-2 -r -R 2>/dev/null
  xfce4-panel -q 2>/dev/null
  sleep 2
  (nohup xfce4-panel >/dev/null 2>&1 &)
fi
# Only the Desktop folder stays on the wallpaper (it holds the Hermes launcher);
# the home/filesystem/trash shortcuts are XFCE defaults that just add clutter.
for k in show-home show-filesystem show-trash; do
  xfconf-query -c xfce4-desktop -p "/desktop-icons/file-icons/$k" -t bool -s false --create 2>/dev/null
done
gsettings set "net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/" icon-size 40 2>/dev/null
exit 0
