parkit
========
**WARNING: For Patched FreePBX 15 ( Tested on 15.0.23 )** CentOS

Parkit is an open-source directory application used to display parked calls on the CP-8851 display.

Easy Installer
---------------
Login as your user, not asterisk, not root
```
sudo yum install git -y && \
git clone --branch spoonfeed-2.0 https://github.com/shido6/parkit.git && \
cd parkit && \
sudo chmod +x runmefirst.sh && \
sudo ./runmefirst.sh
```

Configuration
---------------
Set these environment variables to configure AMI connection (defaults in parentheses):

| Variable | Default |
|----------|---------|
| `AMI_HOST` | `192.168.10.49` |
| `AMI_PORT` | `5038` |
| `AMI_USER` | `admin` |
| `AMI_PASS` | `password` |

Set them in `/etc/systemd/system/my-parked-calls.service` under `[Service]`:
```
Environment=AMI_HOST=10.0.0.1
Environment=AMI_PASS=your-secret
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
rm -rf parkit
```
Then rerun the install command

Oopsy?
-------
Update credentials via environment variables and restart the service:
```
sudo systemctl edit my-parked-calls
```
Add credential lines under `[Service]`, save, then:
```
sudo systemctl restart my-parked-calls
```

Support
-------
 * [Issues](https://github.com/shido6/parkit/issues)

Authors
-------
 * Developers: Shido Xavier <parkit+shido6@gmail.com>
