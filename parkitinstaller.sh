#!/bin/bash

current_user=$(who am i | awk '{print $1}')
current_user_home=$(getent passwd "$current_user" | cut -d: -f6)

echo "Installing Python 3.6 and mlocate"
sudo yum install python36u-pip mlocate -y

python_bin=/usr/bin/python3.6
if [[ ! -x "$python_bin" ]]; then
    echo "Python 3.6 was not found at $python_bin. Install the python36u packages and retry." >&2
    exit 1
fi

echo "Creating virtual environment as asterisk user"
sudo -u asterisk "$python_bin" -m venv /home/asterisk/myenv

echo "Installing flask and pyst2 in the virtual environment"
sudo -u asterisk /home/asterisk/myenv/bin/pip install flask pyst2

echo "Making the scripts directory within /var/lib/asterisk"
sudo mkdir -p /var/lib/asterisk/scripts
echo "Copying script to /var/lib/asterisk/scripts"
sudo cp -v $current_user_home/parkit/parkit11.py /var/lib/asterisk/scripts/parkit11.py

# Change ownership to asterisk
sudo chown -R asterisk:asterisk /home/asterisk/myenv
sudo chown asterisk:asterisk /var/lib/asterisk/scripts/parkit11.py
sudo chmod +x /var/lib/asterisk/scripts/parkit11.py
sudo chmod +x /home/asterisk/myenv/bin/python3

echo "Updating mlocate database"
sudo updatedb

echo "Create the Service"
# Create the Service
cat <<EOL | sudo tee /etc/systemd/system/my-parked-calls.service >/dev/null
[Unit]
Description=My Parked Calls Service
After=network.target

[Service]
EnvironmentFile=/etc/parkit.env
ExecStart=/home/asterisk/myenv/bin/python /var/lib/asterisk/scripts/parkit11.py
WorkingDirectory=/var/lib/asterisk/scripts
Restart=always
User=asterisk
Group=asterisk
RestartSec=5
ExecStop=/bin/true

[Install]
WantedBy=multi-user.target
EOL

echo "Reload the Daemon and enable the service"
# Reload the Daemon and enable the service
sudo systemctl daemon-reload
sudo systemctl enable my-parked-calls

# Create a root-only environment file for AMI credentials if one does not exist.
if [[ ! -f /etc/parkit.env ]]; then
    sudo install -m 0600 -o root -g root /dev/null /etc/parkit.env
    sudo tee /etc/parkit.env >/dev/null <<'EOF'
# Required Parkit AMI settings. Fill these in before starting the service.
AMI_HOST=
AMI_PORT=5038
AMI_USER=
AMI_PASS=
EOF
fi

sudo chown root:root /etc/parkit.env
sudo chmod 0600 /etc/parkit.env

if sudo grep -Eq '^AMI_HOST=[^[:space:]]+' /etc/parkit.env && \
   sudo grep -Eq '^AMI_USER=[^[:space:]]+' /etc/parkit.env && \
   sudo grep -Eq '^AMI_PASS=.+' /etc/parkit.env; then
    sudo systemctl start my-parked-calls
else
    echo "AMI credentials are not configured in /etc/parkit.env."
    echo "Edit that file, then run: sudo systemctl restart my-parked-calls"
fi

echo "Update the conf files with the new services button"
sudo /home/asterisk/myenv/bin/python "$current_user_home/parkit/dirfix.py"
sudo systemctl status my-parked-calls
