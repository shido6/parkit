# parkit
flask app for listing parked calls

# Using an old version of FreePBX 15 (?) 
# Upgrade pip 
yum install python36u-pip

ln -s /usr/bin/python3.6 /usr/bin/python3

python3 -m pip install --upgrade pip


#
# Install the prereqs and setup a virutal environment

python -m venv myenv

source myenv/bin/activate

pip install flask

# Install the prereqs
pip install pyst2

Edit parkit to use your admin and password found in /etc/asterisk/manager.conf

#Run it!

python parkit11.py

# Add the URL this is using to your 88XX series phone SEPXXXXXXXXXXXX.cnf.xml

<directoryURL>http://IPOFFLASKSERVERHERE:5001/services</directoryURL>

# Reboot Phone
