#!/bin/bash
# Define the commands you want to allow without a password prompt
commands=(
    "/home/$youruser/parkit/parkitinstaller.sh"
    "/bin/bash"
)

# Prepare the sudoers configuration lines
sudoers_lines=()
for command in "${commands[@]}"; do
    sudoers_lines+=("$youruser ALL=(asterisk) NOPASSWD: $command")
done

# Append the lines to the sudoers file
for line in "${sudoers_lines[@]}"; do
    echo "$line" >> /etc/sudoers
done

echo "Sudoers file updated successfully."
