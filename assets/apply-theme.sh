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
# --- DESKTOP CLOCK WIDGET ---------------------------------------------
# Analog clock on the wallpaper (reference look), frameless and out of the
# taskbar: Motif hints drop the title bar, the state atoms keep it sticky,
# below normal windows and absent from the pager/taskbar.
pkill -x xclock 2>/dev/null
( xclock -analog -update 1 -norepeat -background white -foreground black \
    -hd black -hl black -bd white -geometry 160x160+170+75 & )
for i in $(seq 1 30); do
  WID=$(xdotool search --class xclock 2>/dev/null | head -1)
  [ -n "$WID" ] && break
  sleep 0.5
done
if [ -n "$WID" ]; then
  xprop -id "$WID" -f _MOTIF_WM_HINTS 32c -set _MOTIF_WM_HINTS "0x2, 0x0, 0x0, 0x0, 0x0" 2>/dev/null
  xprop -id "$WID" -f _NET_WM_STATE 32a -set _NET_WM_STATE \
    _NET_WM_STATE_SKIP_TASKBAR,_NET_WM_STATE_SKIP_PAGER,_NET_WM_STATE_STICKY,_NET_WM_STATE_BELOW 2>/dev/null
fi
# Only the Desktop folder stays on the wallpaper (it holds the Hermes launcher);
# the home/filesystem/trash icons are XFCE defaults that make the desktop look cluttered.
for k in show-home show-filesystem show-trash show-network; do
  xfconf-query -c xfce4-desktop -p "/desktop-icons/file-icons/$k" -t bool -s false --create 2>/dev/null
done
# Dock proportions closer to the reference than plank's default 48px, and a
# slimmer dock leaves the wallpaper readable.
gsettings set "net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/" icon-size 40 2>/dev/null

exit 0
