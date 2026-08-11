import subprocess


def create_namespaces(command):
    subprocess.run(
        [
            "unshare",
            "--pid",
            "--fork",
            "--mount-proc",
            "--uts",
            "sh",
            "-c",
            "hostname containerlite && exec \"$@\"",
            "containerlite",
            *command,
        ],
        check=True,
    )