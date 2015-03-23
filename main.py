#!/usr/bin/python
import os

import cmd

print os.getlogin()
c = cmd.CmdSSH(os.getlogin(), "127.0.0.1");
if True == c.exists():
    c.execute("ls")
    print c.getoutput()
else:
    print "ssh location does not seem to exist"

a = cmd.CmdAndroid()
if True == a.exists():
    a.pull("/system/media/bootanimation.zip", "/tmp/bootanimation.zip")
    a.execute("ls")
    print a.getoutput()
else:
    print "No Android System Found to test"
