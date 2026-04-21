import time
import math
import json
from cpu_info import get_cpu_info

START = 2
END = 12_000_000

cpu_info = get_cpu_info()
start_time = time.time()

count = 0
for n in range(START, END):
    r = int(math.sqrt(n)) + 1
    for i in range(2, r):
        if n % i == 0:
            break
    else:
        count += 1

elapsed = time.time() - start_time

result = {
    "benchmark": "cpu_single",
    "workload": {
        "numbers_tested": END - START
    },
    "results": {
        "primes_found": count,
        "elapsed_seconds": round(elapsed, 2)
    },
    "system": cpu_info
}

print(json.dumps(result, indent=2))
``
