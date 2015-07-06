RemoteScript
====


I decided to create a framework to execute commands from a Linux installation to another Linux system or android device.  I created a base class for this framework that executes the commands on the local Linux Installation where the python scripts reside on.

The Remote Linux Class, CmdSSH, uses sshpass to allow the Python script to know the remote Linux Box passwords. Clearly this would be a security issues but for in house testing, it should be fine.   If you do not specify a password, then it will be assumed the ssh keys are set up correctly.  The script also assumes ECDSA key fingerprint has already been added to known_hosts.

The Android Device Class, CmdAndroid, uses adb to perform the same functions on an attached Android device.  It is assumed that debug is already turned on.

Started to use a version of this framework to initalize qemu sessions using my klem driver to test virtual 80211 networks.



