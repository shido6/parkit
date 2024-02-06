
# Easy Installer
# python3 parkitinstall.py
# Login as your user, not asterisk, not root

Add the following to /etc/sudoers
```
${youruser}   ALL=(asterisk)	NOPASSWD: /home/${youruserhome/parkit/parkitinstaller.sh
${youruser}   ALL=(asterisk)	NOPASSWD: /bin/bash

```

```
sudo yum install git -y ; git clone --branch spoonfeed-2.0 https://github.com/shido6/parkit.git ; sudo chmod +x ~/parkit/parkitinstaller.sh ; sudo ~/parkit/parkitinstaller.sh

```

