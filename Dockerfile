FROM ubuntu:24.04
# Why Ubuntu? Debian Bullseye ছিল মূল বেস, কিন্তু Ubuntu 24.04 LTS বেশি stable,
# বিগিনার ফ্রেন্ডলি, এবং long-term support পায়। এছাড়া Ubuntu-তে প্যাকেজ
# availability বেশি এবং কমিউনিটি সাপোর্ট বেশি।

ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture i386

RUN apt update && apt install -y \
    xrdp \
    xfce4 \
    xfce4-goodies \
    xorg \
    dbus-x11 \
    sudo \
    curl \
    wget \
    nano \
    net-tools \
    policykit-1 \
    pulseaudio \
    pulseaudio-utils \
    wine \
    wine32 \
    firefox && \
    apt clean && rm -rf /var/lib/apt/lists/*
# Note: firefox-esr ছিল Debian-এর প্যাকেজ, Ubuntu-তে শুধু 'firefox' প্যাকেজ ব্যবহার করা
# হয় যেটি স্বয়ংক্রিয়ভাবে latest stable Firefox দেয়।

# Set root password  
RUN echo "root:root" | chpasswd

RUN sed -i 's/^allowed_users=.*/allowed_users=anybody/' /etc/X11/Xwrapper.config || echo "allowed_users=anybody" >> /etc/X11/Xwrapper.config

RUN echo "startxfce4" > /root/.xsession && chmod 700 /root/.xsession

# Generate machine-id for dbus
RUN mkdir -p /var/run/dbus && dbus-uuidgen > /var/lib/dbus/machine-id

RUN sed -i 's/crypt_level=high/crypt_level=low/' /etc/xrdp/xrdp.ini && \
    sed -i 's/security_layer=negotiate/security_layer=rdp/' /etc/xrdp/xrdp.ini && \
    echo "exec startxfce4" > /etc/xrdp/startwm.sh && chmod +x /etc/xrdp/startwm.sh

RUN adduser xrdp ssl-cert

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3389

CMD ["/start.sh"]