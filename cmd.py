#
# Copyright (C) 2015 Stuart Wells <swells@stuartwells.net> All rights reserved.
#
# Licensed under the GNU General Public License, version 2 (GPLv2)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
import os
import shellclass

# For a framework, I might want to have an abstract class
# in this case, the base class just issues commands to a shell
class CmdBase:
    shell = shellclass.SystemShell();
    cmderrno = 0;
    cmddata = ""

    def __init__(self):
        print "start class"
        lasterrno = 0;
        lastdata = ""

    def exists(self):
        return True

    def push(self, input, output):
        # Assume we failed
        rtncode = -1

        # Make sure were passed a string.
        if True == isinstance(input, str) and True == isinstance(output, str):
            # make sure the source is a file
            if True == os.path.isfile(input) and "" != output:
                cmdline = "cp " + input + " " + output
                rtncode = self.shell.execute(cmdline)

        return rtncode

    def pull(self, input, output):
        return self.push(input, output);

    def execute(self, command):
        rtncode = self.shell.execute(command)
        self.cmderrno = self.shell.errno()
        self.cmddata = self.shell.output()

        return rtncode

    def getoutput(self):
        return self.cmddata

# Class to support using ssh to issue commands
class CmdSSH(CmdBase):
    user = ""
    machine = "localhost"
    passwd = ""
    ssh = "/usr/bin/ssh"
    sshpass = "/usr/bin/sshpass"
    scp = "/usr/bin/scp"

    def __init__(self, user, machine, passwd=""):
        CmdBase.__init__(self)
        self.user = user
        self.machine = machine
        self.passwd = passwd
        if "" != passwd:
            if False == os.path.isfile("/usr/bin/sshpass"):
                print "This mechanism requires sshpass to be installed"

    # Does the machine exist?
    def exists(self):
        rtncode = False
        if "Darwin" == os.uname()[0]:
            command = "ping -c 1 " + self.machine
        else:
            command = "ping " + self.machine + " -c 1"

        rval = self.shell.execute(command);
        if 0 == rval:
            rtncode = True

        return rtncode

    def push(self, input, output):
        # Assume we failed
        rtncode = -1
        cmdline = ""

        # Make sure were passed a string.
        if True == isinstance(input, str) and True == isinstance(output, str):
            # make sure the source is a file
            if True == os.path.isfile(input) and "" != output:
                if "" != self.passwd:
                    cmdline += self.sshpass + " -p " + self.passwd + " "
                cmdline += self.scp + " "
                cmdline += input + " "
                cmdline += self.user + "@" + self.machine + ":"
                cmdline += output
                rtncode = self.shell.execute(cmdline)

        return rtncode

    def pull(self, input, output):
        # Assume we failed
        rtncode = -1
        cmdline = ""

        # Make sure were passed a string.
        if True == isinstance(input, str) and True == isinstance(output, str):
            # make sure the source is a file
            if "" != input and "" != output:
                if "" != self.passwd:
                    cmdline += self.sshpass + " -p " + self.passwd + " "
                cmdline += self.scp + " "
                cmdline += self.user + "@" + self.machine + ":"
                cmdline += input + " "
                cmdline += output
                rtncode = self.shell.execute(cmdline)

        return rtncode

    def execute(self, command):
        # Start the command line with nothing.
        cmdline = ""

        # Did we define a password, use sshpass
        if "" != self.passwd:
            cmdline += "sshpass -p " + self.passwd + " "

        cmdline += "ssh "
        cmdline += self.user + "@" + self.machine + " "
        cmdline += "\"" + command + "\""
        rtncode = self.shell.execute(cmdline)
        self.cmderrno = self.shell.errno()
        self.cmddata = self.shell.output()

        return rtncode

# subclass to issue commands to an android device
class CmdAndroid(CmdBase):
    adbpath = "adb"

    def __init__(self):
        CmdBase.__init__(self)
        val = self.shell.execute(self.adbpath + " start-server")

    def exists(self):
        devices = []
        rvalue = False

        rtncode = self.shell.execute(self.adbpath + " devices")
        if 0 == rtncode:
            data = self.shell.output()

            # remove stuff that isn't a device number.
            devices = data.split()
            devices.remove('List')
            devices.remove('attached')
            devices.remove('devices')
            devices.remove('of')

            # Do we have devices connected
            if len(devices) > 0:
                rvalue = True

        return rvalue;

    def push(self, input, output):
        # Assume we failed
        rtncode = -1
        cmdline = ""

        # Make sure were passed a string.
        if True == isinstance(input, str) and True == isinstance(output, str):
            # make sure the source is a file
            if True == os.path.isfile(input) and "" != output:
                cmdline = self.adbpath + " push "
                cmdline += input + " "
                cmdline += output
                rtncode = self.shell.execute(cmdline)

        return rtncode

    def pull(self, input, output):
        # Assume we failed
        rtncode = -1
        cmdline = ""

        # Make sure were passed a string.
        if True == isinstance(input, str) and True == isinstance(output, str):
            # make sure the source is a file
            if "" != input and "" != output:
                cmdline = self.adbpath + " pull "
                cmdline += input + " "
                cmdline += output
                rtncode = self.shell.execute(cmdline)

        return rtncode

    def execute(self, command):
        # Start the command line with nothing.
        cmdline = self.adbpath + " shell "

        # Did we define a password, use sshpass
        cmdline += "\"" + command + "\""

        rtncode = self.shell.execute(cmdline)
        self.cmderrno = self.shell.errno()
        self.cmddata = self.shell.output()

        return rtncode
