import subprocess


def create_pid_namespace(command):
    subprocess.run(
        [
            "unshare",
            "--pid",
            "--fork",
            "--mount-proc",
            *command,
        ],
        check=True,
    )