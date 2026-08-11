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

from containerlite.network import (
    create_veth,
    cleanup_network,
)


def create_container(command, memory_limit="100M", process_limit=20):
    rootfs = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "rootfs")
    )

    create_cgroup()
    set_process_limit(process_limit)
    set_memory_limit(memory_limit)
    set_cpu_limit(50000)

    read_fd, write_fd = os.pipe()

    def enter_cgroup():
        with open(
            os.path.join(CGROUP_PATH, "cgroup.procs"),
            "w",
        ) as f:
            f.write(str(os.getpid()))

    process = None

    try:
        process = subprocess.Popen(
            [
                "unshare",
                "--pid",
                "--fork",
                "--mount",
                "--net",
                "--uts",
                "python3",
                "-c",
                """
import os
import subprocess
import sys

ready_fd = int(os.environ["CONTAINERLITE_NETWORK_FD"])
os.read(ready_fd, 1)

subprocess.run(
    ["mount", "--make-rprivate", "/"],
    check=True,
)

subprocess.run(
    ["hostname", "containerlite"],
    check=True,
)

from containerlite.network import configure_container_network

configure_container_network()

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
            env={
                **os.environ,
                "CONTAINERLITE_NETWORK_FD": str(read_fd),
            },
            pass_fds=(read_fd,),
            preexec_fn=enter_cgroup,
        )

        
        create_veth(process.pid)

        os.write(write_fd, b"1")

        exit_code = process.wait()
        return exit_code

    finally:
        os.close(read_fd)
        os.close(write_fd)

        cleanup_network()
        remove_cgroup()