#!/usr/bin/env python3
import time
import json
from cpu_info import get_cpu_info

SIZE = 1_048_676_000 # 1024 * 1024 * 1000
STRIDE = 4096
PASSES = 1000

cpu_info = get_cpu_info()
data = bytearray(SIZE)

start_time = time.time()
checksum = 0

for _ in range(PASSES):
    for i in range(0, SIZE, STRIDE):
        data[i] = (data[i] + 1) % 256
        checksum += data[i]

elapsed = time.time() - start_time

result = {
    "benchmark": "memory",
    "workload": {
        "bytes": SIZE,
        "passes": PASSES
    },
    "results": {
        "checksum": checksum,
        "elapsed_seconds": round(elapsed, 2)
    },
    "system": cpu_info
}

print(json.dumps(result, indent=2))
