import os

CGROUP_ROOT = "/sys/fs/cgroup"
CGROUP_NAME = "containerlite"
CGROUP_PATH = os.path.join(CGROUP_ROOT, CGROUP_NAME)


def create_cgroup():
    os.makedirs(CGROUP_PATH, exist_ok=True)


def set_cpu_limit(quota, period=100000):
    with open(os.path.join(CGROUP_PATH, "cpu.max"), "w") as f:
        f.write(f"{quota} {period}")


def set_memory_limit(limit):
    with open(os.path.join(CGROUP_PATH, "memory.max"), "w") as f:
        f.write(str(limit))


def set_process_limit(limit):
    with open(os.path.join(CGROUP_PATH, "pids.max"), "w") as f:
        f.write(str(limit))


def remove_cgroup():
    os.rmdir(CGROUP_PATH)