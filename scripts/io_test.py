import time
import os
import json
from cpu_info import get_cpu_info

FILE_SIZE_MB = 1024
ITERATIONS = 100

cpu_info = get_cpu_info()
block = b"x" * (1024 * 1024)
filename = "iotest.dat"

start_time = time.time()

for _ in range(ITERATIONS):
    with open(filename, "wb") as f:
        for _ in range(FILE_SIZE_MB):
            f.write(block)
    with open(filename, "rb") as f:
        while f.read(1024 * 1024):
            pass
    os.remove(filename)

elapsed = time.time() - start_time

result = {
    "benchmark": "io",
    "workload": {
        "file_size_mb": FILE_SIZE_MB,
        "iterations": ITERATIONS
    },
    "results": {
        "elapsed_seconds": round(elapsed, 2)
    },
    "system": cpu_info
}

print(json.dumps(result, indent=2))
