parkit
========
**WARNING: For Patched FreePBX 15 ( Tested on 15.0.23 )**

Parkit is an open-source directory application used to display parked calls on the CP-8851 display.

# Easy Installer
# Login as your user, not asterisk, not root
```
sudo yum install git -y && \
git clone --branch spoonfeed-2.0 https://github.com/shido6/parkit.git && \
cd parkit && \
sudo chmod +x runmefirst.sh && \
sudo ./runmefirst.sh
```
Usage
---------------
See who's in what parking lot without leaving your phone display
Park a call
Press the Directory Button to see a list of Parking Lots
Select the parking lot you wish to view
Select the call you wish to connect to, press Dial.

Troubleshooting
---------------
#### parkit directory
Remove the parkit directory
```
rm parkit
```
Then rerun the install command

# update admin password in parkit11.py
# update runmefirst.sh with current dir or an argument to use the dir specified for /parkit/

Support
-------

 * [Homepage](http://starwoodtechnologies.com)
 * [Issues](https://github.com/shido6/parkit/issues)

Authors
-------

 * Developers: Shido Xavier <parkti+shido6@gmail.com>
