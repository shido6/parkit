import os
import subprocess
import socket
import getpass

# Get the current IP address of the system
def get_current_ip():
    try:
        # Create a socket to get the IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return None

current_ip = get_current_ip()

if current_ip:
    print(f"Current IP address: {current_ip}")
else:
    print("Unable to retrieve the current IP address. Please check your network connectivity.")



# Ask the user for their root password
sudo_password = getpass.getpass("Enter your Sudo/Root password: ")

# Upgrade pip
subprocess.run("sudo su -", shell=True)
subprocess.run("sudo_password, shell=True)
#subprocess.run("{sudo_password}", shell=True)
subprocess.run("yum install python36u-pip mlocate -y", shell=True)
subprocess.run("ln -s /usr/bin/python3.6 /usr/bin/python3", shell=True)
subprocess.run("python3 -m pip install --upgrade pip", shell=True)

# Install prerequisites and set up a virtual environment
subprocess.run("python3 -m venv myenv", shell=True)

# Activate the virtual environment
subprocess.run("source myenv/bin/activate", shell=True)
subprocess.run("pip install flask", shell=True)
subprocess.run("pip install pyst2", shell=True)

# Add manager user and password to parkit
# You can do this manually as it requires editing a configuration file

# Get the Git public not private
# Copy to asterisk scripts
subprocess.run("sudo mkdir -p /var/lib/asterisk/scripts/", shell=True)
subprocess.run("cp parkit/parkit11.py /var/lib/asterisk/scripts/parkit11.py", shell=True)

# Move the environment to the asterisk user folder
subprocess.run("tar cf myenv.tar myenv/", shell=True)
subprocess.run("gzip myenv.tar", shell=True)
subprocess.run("mv myenv.tar.gz /home/asterisk", shell=True)
subprocess.run("cd /home/asterisk", shell=True)
subprocess.run("tar -zxvf myenv.tar.gz", shell=True)

# Change ownership to asterisk from your user
subprocess.run("sudo updatedb", shell=True)
subprocess.run("sudo chown -R asterisk:asterisk myenv", shell=True)
subprocess.run("sudo chown -R asterisk:asterisk /home/asterisk/myenv", shell=True)

# Add Execute Permissions
subprocess.run("sudo chmod +x /var/lib/asterisk/scripts/parkit11.py", shell=True)
subprocess.run("chmod +x /home/asterisk/myenv/bin/python3", shell=True)

# For some reason, this doesnt exist so lets create it
subprocess.run( mkdir -p /var/lib/asterisk/scripts , shell=True)

# Create the Service
with open("/etc/systemd/system/my-parked-calls.service", "w") as service_file:
    service_file.write("""[Unit]
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
""")

# Reload the Daemon and enable the service
subprocess.run("sudo systemctl daemon-reload", shell=True)
subprocess.run("sudo systemctl enable my-parked-calls", shell=True)
subprocess.run("sudo systemctl status my-parked-calls", shell=True)

# Start the service if needed
# subprocess.run("sudo systemctl start my-parked-calls", shell=True)

# Configure TFTP directory in SIP[12 characters].cnf.xml with directoryURL
# Replace 'YOUR_FREEPBX_IP' with the actual FreePBX IP address
# Example: subprocess.run("echo '<directoryURL>http://YOUR_FREEPBX_IP:5001/services</directoryURL>' >> /path/to/SIP[12 characters].cnf.xml", shell=True)
