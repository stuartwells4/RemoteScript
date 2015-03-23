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

import datetime
import os
import signal
import subprocess
import time

class SystemShell:
    timeout = 3;
    lasterrno = 0;
    lastdata = ""

    def __init__(self):
        timeout = 3;
        lasterrno = 0;
        lastdata = ""

    # set the timeout for a command to execute.
    def settimeout(self, newtime):
        self.timeout = newtime

    # allow caller to get the errno for last command executed
    def errno(self):
        return self.lasterrno

    # allow caller to get output from last command executed
    def output(self):
        return self.lastdata

    # execute, and just return the
    def execute (self, command):
        # Clear last error
        self.lasterr = 0
        self.lastdata = ""

        # We have a timeout, find outthe current time
        timestart = datetime.datetime.now()
        subcommand = command.split()

        # default code, if the command didn't actually exist
        rtncode = -1

        try:
            data = subprocess.Popen(subcommand, \
                                    stdout = subprocess.PIPE, \
                                    stderr=subprocess.PIPE)
            while data.poll() is None:
                time.sleep(0.5)
                timecurrent = datetime.datetime.now()
                if (timecurrent - timestart).seconds > self.timeout:
                    if "Linux" == os.uname()[0]:
                        os.kill(data.pid, signal.SIGKILL)
                    elif "Darwin" == os.uname()[0]:
                        os.kill(data.pid, signal.SIGKILL)
                    else:
                        os.kill(data.pid, signal.CTRL_C_EVENT)
                        os.waitpid(-1, os.WNOHANG)
                        return 1
            rtncode = data.returncode
            self.lastdata = data.stdout.read()

        except OSError, e:
            self.lasterrno = e.errno

        return rtncode
