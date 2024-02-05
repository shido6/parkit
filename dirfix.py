import subprocess
import re
import socket

# Step 1: Find the target XML files
result = subprocess.run('sudo locate SEPF*.cnf.xml', shell=True, stdout=subprocess.PIPE, text=True)

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

# Step 3 and 4: Process and modify the XML files
for file_path in result.stdout.splitlines():
    try:
        with open(file_path, 'r') as xml_file:
            xml_content = xml_file.read()
            
            # Use regular expressions to find and replace the <directoryURL> tag
            modified_xml_content = re.sub(r'<directoryURL>.*?</directoryURL>', '<directoryURL>http://%s:5001/services</directoryURL>' % current_ip, xml_content)
        
        # Save the modified content back to the XML file
        with open(file_path, 'w') as modified_file:
            modified_file.write(modified_xml_content)

        print("Modified {}".format(file_path))
    except Exception as e:
        print("Error processing {}: {}".format(file_path, e))
