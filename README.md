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
