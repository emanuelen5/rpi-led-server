from pathlib import Path

CPUINFO_PATH = Path("/proc/cpuinfo")


def is_raspberry_pi():
    with open(CPUINFO_PATH) as f:
        for line in f:
            fields = [f.strip() for f in line.split(":")]
            if fields[0] == "Model":
                return "raspberry pi" in fields[1].lower()
        return False
        # raise ValueError("Could not determine if it is a Raspberry Pi")
