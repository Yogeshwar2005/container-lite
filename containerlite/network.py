import subprocess


HOST_IP = "10.0.0.1/24"
CONTAINER_IP = "10.0.0.2/24"


def create_veth(container_pid):
    subprocess.run(
        [
            "ip",
            "link",
            "add",
            "veth-host",
            "type",
            "veth",
            "peer",
            "name",
            "eth0",
        ],
        check=True,
    )

    subprocess.run(
        [
            "ip",
            "link",
            "set",
            "eth0",
            "netns",
            str(container_pid),
        ],
        check=True,
    )

    subprocess.run(
        [
            "ip",
            "addr",
            "add",
            HOST_IP,
            "dev",
            "veth-host",
        ],
        check=True,
    )

    subprocess.run(
        [
            "ip",
            "link",
            "set",
            "veth-host",
            "up",
        ],
        check=True,
    )


def configure_container_network():
    subprocess.run(
        [
            "ip",
            "addr",
            "add",
            CONTAINER_IP,
            "dev",
            "eth0",
        ],
        check=True,
    )

    subprocess.run(
        [
            "ip",
            "link",
            "set",
            "eth0",
            "up",
        ],
        check=True,
    )


def cleanup_network():
    subprocess.run(
        [
            "ip",
            "link",
            "delete",
            "veth-host",
        ],
        check=False,
    )