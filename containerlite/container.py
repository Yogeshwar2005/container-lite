import os
import subprocess

from containerlite.cgroups import (
    create_cgroup,
    set_process_limit,
    set_memory_limit,
    set_cpu_limit,
    remove_cgroup,
    CGROUP_PATH,
)


def create_container(command, memory_limit="100M", process_limit=20):
    rootfs = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "rootfs")
    )

    create_cgroup()
    set_process_limit(process_limit)
    set_memory_limit(memory_limit)
    set_cpu_limit(50000)
    def enter_cgroup():
        with open(
            os.path.join(CGROUP_PATH, "cgroup.procs"),
            "w",
        ) as f:
            f.write(str(os.getpid()))

    process = subprocess.Popen(
        [
            "unshare",
            "--pid",
            "--fork",
            "--mount",
            "--uts",
            "python3",
            "-c",
            """
import os
import subprocess
import sys

subprocess.run(
    ["mount", "--make-rprivate", "/"],
    check=True,
)

subprocess.run(
    ["hostname", "containerlite"],
    check=True,
)

rootfs = sys.argv[2]
command = sys.argv[3:]

from containerlite.filesystem import setup_filesystem

setup_filesystem(rootfs)

os.execvp(command[0], command)
""",
            "--",
            rootfs,
            *command,
        ],
        preexec_fn=enter_cgroup,
    )

    try:
        process.wait()
    finally:
        remove_cgroup()