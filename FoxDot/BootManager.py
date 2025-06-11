"""
Boot manager

Examples

# With the environment variable or the config file

# With a script using the Go() function:

```python
# `my_file.py` content
from FoxDot import *
p1 >> pads([0, 1, 2, 3])
d1 >> play("x-o-")
Go()
```

$ python my_file.py -b
$ python my_file.py --boot

# With a python module:

$ python -m FoxDot -b
$ python -m FoxDot --boot

# With the CLI:

$ FoxDot -b
$ FoxDot --boot
"""

import os
import os.path
import platform
import sys
from subprocess import Popen
from functools import cached_property

import psutil

FOXDOT_ROOT = os.path.dirname(__file__)
FOXDOT_STARTUP_FILE = os.path.join(FOXDOT_ROOT, "osc/Startup.scd")
FOXDOT_CONFIG_FILE = os.path.join(FOXDOT_ROOT, "lib/Settings/conf.txt")


class BaseBooter:
    process_cmd = ["sclang", FOXDOT_STARTUP_FILE]
    process_name = "sclang"
    process = None
    running = False

    @cached_property
    def BOOT_ON_STARTUP(self):
        """Boot on startup via CLI/Env/Config."""
        # Loading from cli
        for arg in sys.argv[1:]:
            if arg in ['-b', '--boot']:
                return True
            if arg.startswith('-') and 'b' in arg:
                # like: FoxDot -pbs startup.py
                return True

        # Loading from env
        env = os.getenv("BOOT_ON_STARTUP")
        if env is not None:
            return env

        # Loading from configfile
        try:
            with open(FOXDOT_CONFIG_FILE) as file:
                contents = file.read()
            code = compile(contents, "FoxDot", "exec")
            exec(code, globals())
        except FileNotFoundError:
            return False
        return bool(globals().get("BOOT_ON_STARTUP"))

    def start(self):
        """Start SuperCollider."""
        print("Operating system unrecognised")

    def stop(self):
        """Stop SuperCollider."""
        if self.running and self.process:
            return self.kill()

    def kill(self):
        """Killl process."""
        if not self.process:
            return

        process = psutil.Process(self.process.pid)
        for children in process.children(recursive=True):
            children.kill()
        process.kill()


class WindowsBooter(BaseBooter):
    def start(self):
        if not (not self.process and not self.running and not self.is_running()):
            return

        sclangloc = os.popen('where /R "C:\\Program Files" sclang.exe').read()
        thiscwd = str(sclangloc)
        ourcwd = thiscwd.replace("\\sclang.exe\n", "")

        self.process_cmd = [sclangloc, FOXDOT_STARTUP_FILE]
        self.process = Popen(self.process_cmd, cwd=ourcwd)
        self.running = True

    def is_running(self):
        for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
            procname = (
                p.info["name"]
                or p.info["exe"]
                and os.path.basename(p.info["exe"]) == self.process_name
                or p.info["cmdline"]
                and p.info["cmdline"][0] == self.process_name
            )
            if procname.startswith(self.process_name):
                self.running = True
                return self.running


class LinuxBooter(BaseBooter):
    def start(self):
        if not (not self.process and not self.running and not self.is_running()):
            return

        self.process = Popen(self.process_cmd, cwd=os.getcwd())
        self.running = True

    def is_running(self):
        for p in psutil.process_iter(attrs=["name", "cmdline"]):
            # print(p);
            procname = (
                p.info["name"]
                or p.info["cmdline"]
                and p.info["cmdline"][0] == self.process_name
            )
            if procname.startswith(self.process_name):
                self.running = True
                return self.running


OS = platform.system()

if OS == "Windows":
    Boot = WindowsBooter()
elif OS == "Linux":
    Boot = LinuxBooter()
else:
    Boot = BaseBooter()
