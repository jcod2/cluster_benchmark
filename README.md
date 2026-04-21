# HTCondor Mini‑Cluster Benchmark & Stress Test Suite

This repository contains a **self‑contained benchmarking and stress‑testing suite** designed for **small HTCondor (High‑Throughput Computing) clusters** used in instructional or experimental environments.

It is intended for clusters consisting of:
- 1 head node
- 3 (or a small number of) execute nodes
- Modest, heterogeneous hardware (e.g., Dell Optiplex 5040/5050/5060)
- ~8 GB RAM per execute node

All workloads are implemented in **pure Python**, require no external libraries, and are orchestrated using **HTCondor DAGMan**.

---

## Design Goals

This suite is designed to:

- Measure **CPU, memory, disk I/O, and scheduler performance**
- Compare performance across **similar but non‑identical nodes**
- Demonstrate **HTCondor job scheduling and queueing behavior**
- Provide **repeatable, defensible benchmarks** suitable for grading
- Expose students to **long‑running, restart‑safe HTC workloads**

Benchmarks use **fixed amounts of work** (not time‑limited loops), so faster machines finish sooner and slower machines take longer.

---

## Repository Structure

```
.
├── scripts/
│   ├── cpu_info.py
│   ├── cpu_parallel.py
│   ├── cpu_single.py
│   ├── io_stress.py
│   ├── memory_stress.py
│   └── stess_test.py
│
├── benchmark.dag
├── cpu_parallel.submit
├── cpu_single.submit
├── memory.submit
├── io.submit
│
├── stress_test.dag
├── stress.submit
│
└── README.md
```

---

## Short Benchmarks (≈ 1–2 Minutes Each)

These benchmarks are orchestrated by **`benchmark.dag`**. Each job is queued **three times** to allow averaging and variance analysis.

### 1. CPU Single‑Core Benchmark (`cpu_single.py`)
- Fixed prime‑checking workload
- Single‑threaded
- Measures sustained integer and branch performance
- Sensitive to CPU generation and clock speed

**Primary metric:** `elapsed_seconds`

---

### 2. CPU Throughput / Parallel Benchmark (`cpu_parallel.py`)
- Fixed integer arithmetic loop
- Multiple jobs queued simultaneously
- Designed to exceed available slots
- Highlights **HTCondor scheduling, throughput, and fairness**

**Primary metric:** `elapsed_seconds`

---

### 3. Memory Stress Benchmark (`memory_stress.py`)
- Fixed number of memory passes over a large byte array
- Uses < 1 GB RAM and is safe for 8 GB nodes
- Exposes memory bandwidth and cache behavior

**Primary metric:** `elapsed_seconds`

---

### 4. Disk I/O Benchmark (`io_test.py`)
- Repeated fixed‑size write/read/delete cycles
- Measures sustained filesystem and disk performance
- Highly effective at revealing HDD vs SSD differences

**Primary metric:** `elapsed_seconds`

---

## Long‑Running Stress Test (10–60 Minutes)

The stress test is defined separately and is orchestrated by **`stress_test.dag`**.

### Stress Test (`stress_test.py`)

This test simulates a realistic long‑running HTC workload:

- Fixed total number of computational steps
- Mixed CPU and memory activity
- Maximum memory usage ≈ 1 GB
- Periodic checkpointing to disk
- Safe to preempt, evict, or restart
- Multiple jobs may run concurrently

Checkpoint files allow jobs to resume automatically if interrupted.

**Primary metric:** `elapsed_seconds`

---

## Checkpointing Behavior

The stress test writes a JSON checkpoint file at regular intervals containing:
- Current progress step
- Partial checksum
- Original job start time

If a job is restarted, it resumes automatically from the most recent checkpoint and continues accumulating total runtime.

This demonstrates:
- Fault tolerance
- The cost of checkpointing
- Realistic long‑running HTC job design

---

## Standardized CPU & System Reporting

All benchmarks and stress tests emit **structured JSON output** with a consistent schema.

Each job records:
- Execute node hostname
- CPU model name
- CPU frequency information
- Core and thread counts
- Cache sizes
- Kernel and architecture

This information is collected **inside the job** using `lscpu`, ensuring accurate per‑job hardware identification even on heterogeneous clusters.

### Example Output Structure

```json
{
  "benchmark": "cpu_single",
  "workload": { ... },
  "results": {
    "elapsed_seconds": 83.42
  },
  "system": {
    "hostname": "compute-02",
    "model_name": "Intel(R) Core(TM) i5-6500 CPU @ 3.20GHz",
    "cpu_max_mhz": "3200.0000",
    "cpu_s": "4",
    "core_s_per_socket": "4",
    "thread_s_per_core": "1"
  }
}
```

---

## Running the Benchmarks

### Short Benchmarks

```bash
condor_submit_dag benchmark.dag
```

### Long Stress Test

```bash
condor_submit_dag stress_test.dag
```

Monitor execution with:

```bash
condor_q
condor_job_queue_stats
```

---

## Interpreting Results

Because each benchmark performs **the same fixed amount of work**, comparisons are based on:

- Lower runtime → better performance
- Variability across runs → system noise or contention
- Differences across nodes → hardware effects

Students are encouraged to compute:
- Means and standard deviations
- Speedups relative to a baseline node
- Scheduler throughput metrics

---

## Safety and Resource Limits

- All jobs are non‑privileged user processes
- Memory usage is explicitly capped
- Disk usage is temporary and cleaned automatically
- Stress test includes runtime limits in submit files

These benchmarks are safe to run on shared instructional clusters.

---

## Educational Use

This suite is designed for:
- Undergraduate HTC / distributed systems courses
- Introductory cluster computing labs
- Scheduler and systems performance experiments

Instructors are encouraged to adapt parameters and workloads to suit their environment.

---

## License

This code is intended for **educational use**. You are free to modify and redistribute it for teaching and academic purposes.

---

If you have suggestions or improvements, feel free to extend this suite.
