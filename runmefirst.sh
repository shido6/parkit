#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

current_user=$(who am i | awk '{print $1}')
current_user_home=$(getent passwd "$current_user" | cut -d: -f6)

# Create sudoers drop-in so the installer can run commands as the asterisk user
echo "$current_user ALL=(asterisk) NOPASSWD: $current_user_home/parkit/parkitinstaller.sh" > /etc/sudoers.d/parkit
chmod 440 /etc/sudoers.d/parkit

echo "Running parkitinstaller.sh..."
chmod +x "$current_user_home/parkit/parkitinstaller.sh"
sudo -u "$current_user" "$current_user_home/parkit/parkitinstaller.sh"
