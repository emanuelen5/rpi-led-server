from enum import IntEnum
import os
import socket
import subprocess


class KeyCode(IntEnum):
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    UP_ARROW = 65362
    DOWN_ARROW = 65364

    def __repr__(self):
        return self.name


def get_ip():
    if os.name == "nt":
        return socket.gethostbyname(socket.gethostname())
    else:
        p = subprocess.run("hostname -I", capture_output=True, shell=True, encoding="utf-8")
        return p.stdout.strip()
