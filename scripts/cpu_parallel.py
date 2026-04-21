import time
import json
from cpu_info import get_cpu_info

ITERATIONS = 1_000_000_000

cpu_info = get_cpu_info()
start_time = time.time()

x = 0
for i in range(ITERATIONS):
    x += (i % 7) * (i % 13)

elapsed = time.time() - start_time

result = {
    "benchmark": "cpu_parallel",
    "workload": {
        "iterations": ITERATIONS
    },
    "results": {
        "checksum": x,
        "elapsed_seconds": round(elapsed, 2)
    },
    "system": cpu_info
}

print(json.dumps(result, indent=2))
