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
# Remove the default bottom panel so the layout matches the reference (left dock only).
# NOTE: xfconf-query has no --force flag for reset, so use a plain recursive reset.
xfconf-query -c xfce4-panel -p /panels/panel-2 -r -R 2>/dev/null
# Fallback: if the panel object still exists, auto-hide it so it never shows.
if xfconf-query -c xfce4-panel -p /panels/panel-2 >/dev/null 2>&1; then
  xfconf-query -c xfce4-panel -p /panels/panel-2/autohide-behavior -t int -s 2 --create 2>/dev/null
fi
xfce4-panel -r 2>/dev/null
exit 0
