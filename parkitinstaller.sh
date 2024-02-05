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
echo "Create virtual environment myenv python"
sudo python3 -m venv /home/asterisk/myenv
sudo -u $current_user python3 -m venv /home/asterisk/myenv

# Activate the virtual environment
echo "Installing flask and pyst2"
#sudo source $current_user_home/myenv/bin/activate
source /home/asterisk/myenv/bin/activate
#sudo /bin/bash -c "source /home/asterisk/myenv/bin/activate"
 pip install flask pyst2 asterisk
 deactivate

echo "Making the scripts directory within /var/lib/asterisk"
sudo mkdir -p /var/lib/asterisk/scripts
echo "Copying script to /var/lib/asterisk/scripts"
sudo cp -v $current_user_home/parkit/parkit11.py /var/lib/asterisk/scripts/parkit11.py

#echo "Changing ownership and moving files to headless asterisk user"
# Move the environment to the asterisk user folder
#sudo tar -zcvf myenv.tar.gz $current_user_home/myenv/
#sudo mv myenv.tar.gz /home/asterisk/

# Extract myenv.tar.gz in /home/asterisk
#echo "Extracting myenv.tar.gz in /home/asterisk"
#cd /home/asterisk
#sudo tar -zxvf myenv.tar.gz

# Check if the myenv directory exists
myenv_directory="$current_user_home/myenv"
if [ ! -d "$myenv_directory" ]; then
    echo "Error: The myenv directory does not exist."
    exit 1
fi

# Move the myenv directory to /home/asterisk
echo "Moving the myenv directory to /home/asterisk"
sudo mv "$myenv_directory" /home/asterisk/

# Verify that myenv is now in /home/asterisk
if [ -d "/home/asterisk/myenv" ]; then
    echo "Successfully moved myenv to /home/asterisk"
else
    echo "Error: Failed to move myenv to /home/asterisk."
    exit 1
fi

# Create myenv.tar.gz
echo "Creating myenv.tar.gz"
sudo tar -zcvf /home/asterisk/myenv.tar.gz -C /home/asterisk myenv

# Verify that myenv.tar.gz is now in /home/asterisk
if [ -f "/home/asterisk/myenv.tar.gz" ]; then
    echo "Successfully created myenv.tar.gz in /home/asterisk"
else
    echo "Error: Failed to create myenv.tar.gz in /home/asterisk."
    exit 1
fi

# Extract myenv.tar.gz in /home/asterisk
echo "Extracting myenv.tar.gz in /home/asterisk"
cd /home/asterisk
sudo tar -zxvf myenv.tar.gz

# Verify that myenv is now extracted in /home/asterisk
if [ -d "/home/asterisk/myenv" ]; then
    echo "Successfully extracted myenv in /home/asterisk"
else
    echo "Error: Failed to extract myenv in /home/asterisk."
    exit 1
fi

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
ExecStart=/bin/bash -c ". /home/asterisk/myenv/bin/activate && /home/asterisk/myenv/bin/python3 /var/lib/asterisk/scripts/parkit11.py"
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
