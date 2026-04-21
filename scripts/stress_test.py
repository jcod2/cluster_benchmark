import time
import json
import os
import math
import random
from cpu_info import get_cpu_info

# =========================
# CONFIGURATION (CALIBRATE ONCE)
# =========================

TOTAL_STEPS = 2_000_000_000
CHECKPOINT_INTERVAL = 1_000_000   # save state every N steps
ARRAY_SIZE = 120_000_000          # ~120 MB
STATE_FILE = "stress_state.json"
RESULT_FILE = "stress_result.json"

# =========================
# INITIALIZATION
# =========================

data = bytearray(ARRAY_SIZE)

def cpu_work(x):
    return math.sin(x) * math.cos(x) + math.sqrt(abs(x))

def memory_work(idx):
    idx = idx % ARRAY_SIZE
    data[idx] = (data[idx] + 1) % 256
    return data[idx]

# =========================
# LOAD CHECKPOINT (IF ANY)
# =========================

step = 0
checksum = 0
start_time = time.time()

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
        step = state["step"]
        checksum = state["checksum"]
        start_time = state["start_time"]

# =========================
# MAIN WORK LOOP
# =========================

for i in range(step, TOTAL_STEPS):
    # CPU-bound work
    x = cpu_work(i)

    # Memory-bound work
    m = memory_work(i)

    checksum += int(x * 1000) + m

    # Checkpoint periodically
    if i % CHECKPOINT_INTERVAL == 0 and i > step:
        with open(STATE_FILE, "w") as f:
            json.dump({
                "step": i,
                "checksum": checksum,
                "start_time": start_time
            }, f)

total_time = time.time() - start_time

# =========================
# FINAL OUTPUT
# =========================

cpu_info = get_cpu_info()

# included unchanged: checkpoint loading and main loop

result = {
    "benchmark": "stress_test",
    "workload": {
        "total_steps": TOTAL_STEPS,
        "checkpoint_interval": CHECKPOINT_INTERVAL
    },
    "results": {
        "final_checksum": checksum,
        "elapsed_seconds": round(total_time, 2),
        "completed": True
    },
    "system": cpu_info
}

with open(RESULT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
