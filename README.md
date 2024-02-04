# parkit version 11
flask app for listing parked calls

# Using an old version of FreePBX 15 (?) 
# Tested on FreePBX 15.0.23
# Upgrade pip 
```
yum install python36u-pip
ln -s /usr/bin/python3.6 /usr/bin/python3
python3 -m pip install --upgrade pip
```

# Install the prereqs and setup a virutal environment
```
python3 -m venv myenv
```
# Activate the virtual environment
```
source myenv/bin/activate
```
```
pip install flask
```
# Install the prereqs
```
pip install pyst2
```
Add your manager user and password found in your FreePBX /etc/asterisk/manager.conf to parkit.

# Copy to asterisk scripts 
```
cp parkit11.py /var/lib/asterisk/scripts/parkit11.py
```
Move the environment to the asterisk user folder
```
tar cf myenv.tar myenv/
gzip myenv.tar
mv myenv.tar.gz /home/asterisk
cd /home/asterisk
tar -zxvf myenv.tar.gz
```
# Change ownership to asterisk from your user
```
sudo chown -R asterisk:asterisk myenv
sudo chown -R asterisk:asterisk /home/asterisk/myenv

```
# Add Execute Permissions
```
sudo chmod +x /var/lib/asterisk/scripts/parkit11.py
chmod +x /home/asterisk/myenv/bin/python3
```
# Create the Service
```
sudo nano /etc/systemd/system/my-parked-calls.service
```
# Add the following to the file
```
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
```
# Reload the Daemon and enable the service
```
sudo systemctl daemon-reload
sudo systemctl enable my-parked-calls
sudo systemctl status my-parked-calls

```
# Start the service if you need to
```
sudo systemctl start my-parked-calls
```
You should see
```
● my-parked-calls.service - My Parked Calls Service
   Loaded: loaded (/etc/systemd/system/my-parked-calls.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2024-01-26 13:53:06 UTC; 1s ago
 Main PID: 12005 (python3)
   CGroup: /system.slice/my-parked-calls.service
           └─12005 /home/asterisk/myenv/bin/python3 /var/lib/asterisk/scripts/parkit11.py

Jan 26 13:53:06 freepbx.sangoma.local systemd[1]: Started My Parked Calls Service.
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: * Serving Flask app 'parkit11' (lazy loading)
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: * Environment: production
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: WARNING: This is a development server. Do not use it in a production deployment.
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: Use a production WSGI server instead.
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: * Debug mode: off
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: * Running on all addresses.
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: WARNING: This is a development server. Do not use it in a production deployment.
Jan 26 13:53:07 freepbx.sangoma.local python3[12005]: * Running on http://192.168.10.49:5001/ (Press CTRL+C to quit)

```


# Add the URL this is using to your 88XX series phone SEPXXXXXXXXXXXX.cnf.xml
```
<directoryURL>http://FREEPBXIP:5001/services</directoryURL>
```
# Reboot Phone
Settings > 7 > 5 > 1
or send a sip notify, etc

# Troubleshooting
Python3 in the asterisk venv needs to be executable!
```
ls -l /home/asterisk/myenv/bin/python3
chmod +x /home/asterisk/myenv/bin/python3
```
