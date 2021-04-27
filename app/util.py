import os
import socket
import subprocess
from util import max_update_rate


def run_command(cmd):
    p = subprocess.run(cmd, capture_output=True, shell=True, encoding="utf-8")
    return p.stdout.strip()


@max_update_rate(1.0)
def get_ips():
    if os.name == "nt":
        return tuple(socket.gethostbyname(socket.gethostname()))
    else:
        return tuple(run_command("hostname -I").split(' '))


@max_update_rate(3.0)
def get_uptime():
    if os.name == "nt":
        return "Unknown"
    else:
        return run_command("uptime")
