import argparse

from .namespaces import create_namespaces


def main():
    parser = argparse.ArgumentParser(
        prog="containerlite",
        description="A lightweight Linux container runtime",
    )
    
    parser.add_argument(
        "--memory",
        default="100M",
        help="Memory limit for the container",
    )

    parser.add_argument(
        "--pids",
        type=int,
        default=20,
        help="Maximum number of processes",
    )

    parser.add_argument(
        "command",
        nargs="+",
        help="Command to run inside the container",
    )

    args = parser.parse_args()

    print("[ContainerLite] Starting container...")
    create_namespaces(
        args.command,
        memory_limit=args.memory,
        process_limit=args.pids,
    )

if __name__ == "__main__":
    main()