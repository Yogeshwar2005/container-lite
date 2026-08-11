import subprocess


def create_namespaces(command):
    subprocess.run(
        [
            "unshare",
            "--pid",
            "--fork",
            "--mount",
            "--uts",
            "sh",
            "-c",
            """
            mount --make-rprivate /
            hostname containerlite
            exec chroot rootfs /bin/sh -c '
            /bin/busybox mount -t proc proc /proc
            exec "$@"
            ' -- "$@"
            """,
            "--",
            *command,
        ],
        check=True,
    )