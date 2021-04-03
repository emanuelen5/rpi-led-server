from enum import IntEnum
import os
import socket
import subprocess
import time


class KeyCode(IntEnum):
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    UP_ARROW = 65362
    DOWN_ARROW = 65364

    def __repr__(self):
        return self.name


def run_command(cmd):
    p = subprocess.run(cmd, capture_output=True, shell=True, encoding="utf-8")
    return p.stdout.strip()


def max_update_rate(update_rate: float = 1.0):
    def wrapper(f):
        f.last_update_time = 0

        def cache_wrapper(*args, **kwargs):
            now = time.time()
            if now - f.last_update_time > update_rate:
                f.cached_value = f(*args, **kwargs)
                f.last_update_time = now
            return f.cached_value

        return cache_wrapper

    return wrapper


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
