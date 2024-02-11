#!/usr/bin/env python3.6

import subprocess
import re
import socket

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

if not current_ip:
    print("Unable to retrieve the current IP address. Please check your network connectivity.")
    exit()

print("Current IP address:", current_ip)

# Run updatedb to update the file database
subprocess.call('sudo updatedb', shell=True)

# Find and update SEP<mac>.cnf.xml files
locate_command = 'sudo locate .cnf.xml'
#!/usr/bin/env python3.6

import subprocess
import re
import socket
import os

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

if not current_ip:
    print("Unable to retrieve the current IP address. Please check your network connectivity.")
    exit()

print("Current IP address:", current_ip)

# Run updatedb to update the file database
subprocess.call(['sudo', 'updatedb'])

# Find and update SEP<mac>.cnf.xml files within /var directories labeled tftp or tftpboot
locate_command = ['sudo', 'locate', '/var/*/tftp', '/var/*/tftpboot']
result = subprocess.Popen(locate_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
stdout, stderr = result.communicate()

if result.returncode == 0:
    for directory_path in stdout.splitlines():
        try:
            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    if file_name.endswith('.cnf.xml'):
                        file_path = os.path.join(root, file_name)
                        with open(file_path, 'r') as xml_file:
                            xml_content = xml_file.read()
                            # Use regular expressions to find and replace the <directoryURL> tag
                            modified_xml_content = re.sub(r'<directoryURL>.*?</directoryURL>', '<directoryURL>http://{0}:5001/services</directoryURL>'.format(current_ip), xml_content)
                            # Save the modified content back to the XML file
                            with open(file_path, 'w') as modified_file:
                                modified_file.write(modified_xml_content)
                            print("Modified {}".format(file_path))
        except Exception as e:
            print("Error processing {}: {}".format(file_path, e))
else:
    print("Error executing 'sudo locate':", stderr)

