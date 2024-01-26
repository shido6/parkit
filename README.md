# parkit
flask app for listing parked calls

# Using an old version of FreePBX 15 (?) 
# Upgrade pip 
yum install python36u-pip

ln -s /usr/bin/python3.6 /usr/bin/python3

python3 -m pip install --upgrade pip


# Install the prereqs and setup a virutal environment

python -m venv myenv

# Activate the virtual environment

source myenv/bin/activate

pip install flask

# Install the prereqs
pip install pyst2

Edit parkit to use your admin and password found in /etc/asterisk/manager.conf

# Copy to asterisk scripts 

cp parkit11.py /var/lib/asterisk/scripts/parkit11.py

Move the environment to the asterisk user folder

tar cf myenv.tar myenv
gzip myenv.tar.gz
mv myenv.tar.gz /home/asterisk
cd /home/asterisk
tar -zxvf myenv.tar.gz

# Change ownership to asterisk from your user

sudo chown -R asterisk:asterisk myenv

# Create the Service

sudo nano /etc/systemd/system/my-parked-calls.service

# Add the following to the file

[Unit]
Description=My Parked Calls Service

After=network.target

[Service]
ExecStart=/home/asterisk/myenv/bin/python3 /var/lib/asterisk/scripts/parkit11.py

WorkingDirectory=/var/lib/asterisk/scripts

Restart=always

User=asterisk

Group=asterisk

RestartSec=5

[Install]
WantedBy=multi-user.target

# Reload the Daemon and enable the service

sudo systemctl daemon-reload

sudo systemctl enable my-parked-calls

# Start the service

sudo systemctl status my-parked-calls


# Add the URL this is using to your 88XX series phone SEPXXXXXXXXXXXX.cnf.xml

<directoryURL>http://IPOFFLASKSERVERHERE:5001/services</directoryURL>

# Reboot Phone
