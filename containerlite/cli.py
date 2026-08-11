import argparse

from .namespaces import create_pid_namespace


def main():
    parser = argparse.ArgumentParser(
        prog="containerlite",
        description="A lightweight Linux container runtime",
    )

    parser.add_argument(
        "command",
        nargs="+",
        help="Command to run inside the container",
    )

    args = parser.parse_args()

    print("[ContainerLite] Starting container...")
    create_pid_namespace(args.command)


if __name__ == "__main__":
    main()