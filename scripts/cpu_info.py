import platform
import subprocess
import socket
import os
import time

def get_cpu_info():
    """
    Returns a dict with standardized CPU and host information.
    Safe to call on HTCondor execute nodes without privileges.
    """
    info = {
        "hostname": socket.gethostname(),
        "kernel": platform.release(),
        "arch": platform.machine()
    }

    try:
        lscpu = subprocess.check_output(["lscpu"], text=True)
        for line in lscpu.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                key = k.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
                info[key] = v.strip()
    except Exception as e:
        info["lscpu_error"] = str(e)

    return info
