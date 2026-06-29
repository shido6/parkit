#!/bin/bash

current_user=$(who am i | awk '{print $1}')
current_user_home=$(getent passwd "$current_user" | cut -d: -f6)

echo "Updating python"
sudo yum install python36u-pip mlocate -y
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
sudo python3 -m pip install --upgrade pip
sudo yum update -y

echo "Creating virtual environment as asterisk user"
sudo -u asterisk python3 -m venv /home/asterisk/myenv

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

# Start the service if needed
sudo systemctl start my-parked-calls

echo "Update the conf files with the new services button"
sudo python $current_user_home/parkit/dirfix.py
sudo systemctl status my-parked-calls
