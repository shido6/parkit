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
        print("Error:", e)
        return None

current_ip = get_current_ip()

if current_ip:
    print("Current IP address:", current_ip)
else:
    print("Unable to retrieve the current IP address. Please check your network connectivity.")


# Ask the user for their sudo password
sudo_password = getpass.getpass("Enter your sudo password: ")

# Upgrade pip
command = 'echo "{}" | sudo -S yum install python36u-pip mlocate -y'.format(sudo_password)
subprocess.call(command, shell=True)
subprocess.call("ln -s /usr/bin/python3.6 /usr/bin/python3", shell=True)
subprocess.call("python3 -m pip install --upgrade pip", shell=True)

# Install prerequisites and set up a virtual environment
subprocess.call("python3 -m venv myenv", shell=True)

# Activate the virtual environment
subprocess.call("source ~/myenv/bin/activate", shell=True)
subprocess.call("pip install flask", shell=True)
subprocess.call("pip install pyst2", shell=True)

# Add manager user and password to parkit
# You can do this manually as it requires editing a configuration file

# Get the Git public not private
# Copy to asteri

command1 = 'echo "{}" | sudo -S mkdir -p /var/lib/asterisk/scripts'.format(sudo_password)
subprocess.call(command1, shell=True)

subprocess.call("cp -v ~/parkit/parkit11.py /var/lib/asterisk/scripts/parkit11.py", shell=True)

# Move the environment to the asterisk user folder
subprocess.call("tar -zcvf /home/asterisk/myenv.tar.gz ~/myenv/", shell=True)
# Change ownership to asterisk (with verbosity)
subprocess.call("sudo chown -Rv asterisk:asterisk /home/asterisk/myenv", shell=True)
subprocess.call("sudo chown -v asterisk:asterisk /var/lib/asterisk/scripts/parkit11.py", shell=True)
subprocess.call("sudo chmod -v +x /var/lib/asterisk/scripts/parkit11.py", shell=True)
subprocess.call("sudo chmod -v +x /home/asterisk/myenv/bin/python3", shell=True)
subprocess.call("updatedb", shell=True)

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
subprocess.call("sudo systemctl daemon-reload", shell=True)
subprocess.call("sudo systemctl enable my-parked-calls", shell=True)
subprocess.call("sudo systemctl status my-parked-calls", shell=True)

# Start the service if needed
# subprocess.call("sudo systemctl start my-parked-calls", shell=True)

# Configure TFTP directory in SIP[12 characters].cnf.xml with directoryURL
# Replace 'YOUR_FREEPBX_IP' with the actual FreePBX IP address
# Example: subprocess.call("echo '<directoryURL>http://YOUR_FREEPBX_IP:5001/services</directoryURL>' >> /path/to/SIP[12 characters].cnf.xml", shell=True)
