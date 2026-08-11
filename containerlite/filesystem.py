import os
import subprocess


def setup_filesystem(rootfs):
    os.chroot(rootfs)
    os.chdir("/")

    subprocess.run(
        ["/bin/busybox", "mount", "-t", "proc", "proc", "/proc"],
        check=True,
    )