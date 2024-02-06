#!/bin/bash

# Get the current IP address of the system
get_current_ip() {
    ip_address=$(ip route get 8.8.8.8 | awk '{print $NF; exit}')
    echo "$ip_address"
}

current_ip=$(get_current_ip)

if [ -n "$current_ip" ]; then
    echo "Current IP address: $current_ip"
else
    echo "Unable to retrieve the current IP address. Please check your network connectivity."
fi

# Get the current user
current_user=$(who am i | awk '{print $1}')
current_user_home=$(getent passwd "$current_user" | cut -d: -f6)
echo "Current user: $current_user"
echo "Home directory: $current_user_home"

# Upgrade pip
echo "Updating python"
sudo yum install python36u-pip mlocate -y
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
sudo python3 -m pip install --upgrade pip
sudo yum update -y


# Install prerequisites and set up a virtual environment
echo "Updating virtual environmnet activate permissions"
sudo chmod +x /home/asterisk/myenv/bin/activate

echo "Changing to user asterisk"
sudo -u asterisk /bin/bash << EOF
  # Activate the virtual environment
  echo "Activating virtual environment myenv"
  python3 -m venv /home/asterisk/myenv
  source /home/asterisk/myenv/bin/activate

  # Install prerequisites and set up a virtual environment
  echo "Installing flask, pyst2, and asterisk in the virtual environment"
  pip install flask pyst2 asterisk

  # Deactivate the virtual environment
  echo "Deactivating virtual environment"
  deactivate
EOF

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
sudo systemctl status my-parked-calls

# Start the service if needed
sudo systemctl start my-parked-calls

echo "Update the conf files with the new services button"
sudo python $current_user_home/parkit/dirfix.py
