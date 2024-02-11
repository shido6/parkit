
# Easy Installer
# Login as your user, not asterisk, not root
```
sudo yum install git -y && \
git clone --branch spoonfeed-2.0 https://github.com/shido6/parkit.git && \
cd parkit && \
sudo chmod +x runmefirst.sh && \
sudo ./runmefirst.sh
```
# Phone Application for CP-8851 Cisco Phones
For Patched FreePBX 15 ( Tested on 15.0.23 )

See who's in what parking lot without leaving your phone display

Press the Directory Button to see a list of Parking Lots
Select the parking lot you wish to view
Select the call you wish to connect to.
# Troubleshooting
Remove the parkit directory
```
rm parkit
```
Then rerun the install command
update admin password in parkit11.py
