#!/bin/bash

USER_PREF=dji

###############################################################################
### Basic System Setup:
###############################################################################

# Localization changes and keyboard setup moved to dietpi.txt autoconfiguration
echo "djiplayer" > /etc/hostname

###############################################################################
### Add personalization:
###############################################################################


###############################################################################
### Install required packages and environment:
###############################################################################
# Superfluous with autosetup installation with DietPi
apt -y install \
    python3-pip \
    git 
pip3 install pyusb

###############################################################################
### Configure the User:
###############################################################################

useradd \
    -d /home/${USER_PREF} \
    -m \
    -p dji.1234 \
    -s /bin/bash \
    ${USER_PREF}


###############################################################################
### Configure auto-login:
###############################################################################
sed -i -e "s/AUTO_SETUP_AUTOSTART_LOGIN_USER=.*/AUTO_SETUP_AUTOSTART_LOGIN_USER=${USER_PREF}/" /boot/dietpi.txt
/boot/dietpi/dietpi-autostart 2

###############################################################################
### Install the player wrapper:
###############################################################################

git clone https://github.com/hcardwell/usb-vsp.git /home/${USER_PREF}/player

mkdir -p /home/${USER_PREF}/.config/autostart
cat << _EOF_ > /home/${USER_PREF}/.config/autostart/player.desktop
[Desktop Entry]
Type=Application
Exec=/usr/bin/lxterminal -e /home/${USER_PREF}/wrap.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=term
Name=term
Comment[en_US]=
Comment=
_EOF_

cat << _EOF_ > /home/${USER_PREF}/wrap.sh
#!/bin/bash

echo "###############################################################################"
echo "###############################################################################"
echo "### Starting DJI Player"
echo "###############################################################################"
echo "###############################################################################"


# Disable the screensaver and whatnot:
which gsettings >/dev/null 2>&1
if [ $? -eq 0 ] ; then
    gsettings set org.gnome.desktop.screensaver lock-delay 3600
    gsettings set org.gnome.desktop.screensaver lock-enabled false
    gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
fi

# echo "mbuffer -I 5000 -o - | ffplay -i - -analyzeduration 1 -probesize 32 -sync ext"

xset -dpms
xset s off

cd /home/${USER_PREF}/player
exec /usr/bin/python3 djiplayer.py

_EOF_

cat << _EOF_ > /etc/udev/rules.d/52-dji.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="2ca3", MODE="0666", GROUP="plugdev"
_EOF_

# Fix permissions we broke above:
chown -R ${USER_PREF}:${USER_PREF} \
    /home/${USER_PREF}/player \
    /home/${USER_PREF}/.config \
    /home/${USER_PREF}/wrap.sh

chmod +x /home/${USER_PREF}/wrap.sh

echo "Reboot Now, configure autologin to LXDE as user '${USER_PREF}'"


