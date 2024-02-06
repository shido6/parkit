#!/bin/bash

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

# Get the current user
current_user=$(who am i | awk '{print $1}')
current_user_home=$(getent passwd "$current_user" | cut -d: -f6)
echo "Current user: $current_user"
echo "Home directory: $current_user_home"

# Define the commands you want to allow without a password prompt
commands=(
    "/home/$current_user/parkit/parkitinstaller.sh"
    "/bin/bash"
)

# Prepare the sudoers configuration lines
sudoers_lines=()
for command in "${commands[@]}"; do
    sudoers_lines+=("$current_user ALL=(asterisk) NOPASSWD: $command")
done

# Append the lines to the sudoers file
for line in "${sudoers_lines[@]}"; do
    echo "$line" >> /etc/sudoers
done

echo "Sudoers file updated successfully."

# Run the parkitinstaller.sh script
echo "Running parkitinstaller.sh..."
sudo -u $current_user $current_user_home/parkit/parkitinstaller.sh
