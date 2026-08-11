import os
import subprocess


def create_namespaces(command):
    rootfs = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "rootfs")
    )

    subprocess.run(
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

subprocess.run(["mount", "--make-rprivate", "/"], check=True)

subprocess.run(["hostname", "containerlite"], check=True)

rootfs = sys.argv[2]
command = sys.argv[3:]

os.chroot(rootfs)
os.chdir("/")

subprocess.run(
    ["/bin/busybox", "mount", "-t", "proc", "proc", "/proc"],
    check=True,
)

os.execvp(command[0], command)
""",
            "--",
            rootfs,
            *command,
        ],
        check=True,
    )