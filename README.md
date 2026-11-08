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
Parkit requires an AMI account. Create a dedicated AMI user with read/call
permissions rather than using `admin`.

The installer creates `/etc/parkit.env` with mode `0600` if it does not exist.
Set these values:

| Variable | Required | Default |
|----------|----------|---------|
| `AMI_HOST` | yes | none |
| `AMI_PORT` | no | `5038` |
| `AMI_USER` | yes | none |
| `AMI_PASS` | yes | none |

```bash
sudoedit /etc/parkit.env
```
```text
AMI_HOST=10.0.0.1
AMI_PORT=5038
AMI_USER=parkit
AMI_PASS=your-secret
```

The service reads this file through `EnvironmentFile=/etc/parkit.env`. Parkit
will not start if `AMI_HOST`, `AMI_USER`, or `AMI_PASS` is empty.

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
Update credentials in `/etc/parkit.env`, then restart the service:
```
sudoedit /etc/parkit.env
sudo systemctl restart my-parked-calls
```

Support
-------
 * [Issues](https://github.com/shido6/parkit/issues)

Authors
-------
 * Developers: Shido Xavier <parkit+shido6@gmail.com>
