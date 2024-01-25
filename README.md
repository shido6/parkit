# parkit
flask app for listing parked calls
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

<directoryURL>http://IPOFFLASKSERVERHERE:5000/services</directoryURL>

# Reboot Phone
