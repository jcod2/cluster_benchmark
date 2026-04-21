"""
cpu_info.py

Helper module for collecting standardized CPU and system metadata
on HTCondor execute nodes. Intended for instructional benchmarking
and stress‑testing workloads.

Requires:
  - Python 3
  - lscpu available in PATH (standard on Linux)

No special privileges required.
"""

import platform
import subprocess
import socket

def get_cpu_info():
    """
    Collects CPU and basic system information using platform info
    and the `lscpu` command.

    Returns
    -------
    dict
        A dictionary of normalized system and CPU attributes.
    """
    info = {
        "hostname": socket.gethostname(),
        "arch": platform.machine(),
        "kernel": platform.release()
    }

    try:
        output = subprocess.check_output(["lscpu"], text=True)
        for line in output.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            norm_key = (
                key.strip()
                .lower()
                .replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
            )
            info[norm_key] = value.strip()
    except Exception as e:
        info["lscpu_error"] = str(e)

    return info


if __name__ == "__main__":
    # Simple CLI test mode
    import json
    print(json.dumps(get_cpu_info(), indent=2))
