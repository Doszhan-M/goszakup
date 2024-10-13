#!/bin/bash


if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

sudo apt-get update
sudo apt-get install -y python3-tk python3-dev xclip dbus-x11 xvfb x11vnc xdotool gnome-screenshot
sudo reboot
