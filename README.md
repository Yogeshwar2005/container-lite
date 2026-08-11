# ContainerLite

A lightweight Linux container runtime built from scratch in Python to understand how Linux containers work internally.

ContainerLite uses Linux **namespaces**, **cgroups v2**, **chroot**, **BusyBox**, and **veth networking** to provide process, filesystem, hostname, network, and resource isolation.

---

## Features

### Linux Namespaces

ContainerLite uses Linux namespaces to isolate the container from the host:

* **PID namespace** — processes inside the container have their own PID hierarchy.
* **Mount namespace** — container mount changes are isolated from the host.
* **UTS namespace** — the container has its own hostname.
* **Network namespace** — the container gets an isolated network stack.

### Filesystem Isolation

* Uses `chroot` to provide a separate root filesystem.
* Uses a minimal **BusyBox-based rootfs**.
* Mounts `/proc` inside the container.
* Provides common Unix commands through BusyBox symlinks.

### Resource Limits

Uses **cgroups v2** to limit container resources:

* Memory limit
* CPU limit
* Maximum number of processes

Cgroups are automatically removed when the container exits.

### Networking

ContainerLite creates a **veth pair** between the host and container network namespaces.

```text
                HOST
              10.0.0.1
                  │
              veth-host
                  │
             ┌────┴────┐
             │  veth   │
             └────┬────┘
                  │
                eth0
              10.0.0.2
              CONTAINER
```

The container can communicate with the host through the virtual Ethernet pair.

### Exit Code Propagation

ContainerLite propagates the exit status of the process executed inside the container.

For example:

```bash
sudo python3 -m containerlite -- /bin/sh -c 'exit 42'
echo $?
```

returns:

```text
42
```

---

## Project Structure

```text
container-lite/
│
├── containerlite/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── container.py
│   ├── namespaces.py
│   ├── filesystem.py
│   ├── cgroups.py
│   └── network.py
│
├── rootfs/
│   ├── bin/
│   │   └── busybox
│   ├── proc/
│   └── tmp/
│
├── scripts/
│   └── setup_rootfs.sh
│
└── README.md
```

---

## Requirements

ContainerLite currently targets Linux systems and requires:

* Linux
* Python 3
* `sudo` / root privileges
* Linux namespaces
* cgroups v2
* `unshare`
* BusyBox

Check that cgroups v2 is available:

```bash
mount | grep cgroup
```

You should see something similar to:

```text
cgroup2 on /sys/fs/cgroup type cgroup2
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Yogeshwar2005/container-lite.git
cd container-lite
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install BusyBox

On Debian/Ubuntu:

```bash
sudo apt install busybox-static
```

### 4. Create the root filesystem

Run:

```bash
./scripts/setup_rootfs.sh
```

This copies BusyBox into `rootfs/bin` and creates symlinks for the commands provided by BusyBox.

---

## Usage

Run a simple command:

```bash
sudo python3 -m containerlite /bin/echo hello
```

Output:

```text
[ContainerLite] Starting container...
hello
```

Start an interactive shell:

```bash
sudo python3 -m containerlite /bin/sh
```

Inside the container:

```bash
/ #
```

---

## Command Options

### Memory Limit

The default memory limit is `100M`.

```bash
sudo python3 -m containerlite --memory 200M /bin/sh
```

### Process Limit

The default maximum number of processes is `20`.

```bash
sudo python3 -m containerlite --pids 50 /bin/sh
```

### Commands with Arguments

Use `--` to separate ContainerLite options from the command's arguments:

```bash
sudo python3 -m containerlite -- /bin/sh -c 'echo hello && echo world'
```

This is particularly important for commands such as `sh -c` that have their own command-line options.

---

## Testing Isolation

### PID Namespace

Inside the container:

```bash
echo $$
```

The container's init process should have PID:

```text
1
```

You can also check:

```bash
cat /proc/1/status | grep NSpid
```

---

### UTS Namespace

Inside:

```bash
hostname
```

Expected:

```text
containerlite
```

The host's hostname remains unchanged.

---

### Network Namespace

Inside:

```bash
ip link
```

The container should have its own network interfaces, including:

```text
lo
eth0
```

Check the container IP:

```bash
ip addr
```

The current networking setup uses:

```text
Container: 10.0.0.2
Host:      10.0.0.1
```

Test connectivity:

```bash
ping -c 3 10.0.0.1
```

---

### Cgroups

ContainerLite creates a cgroup at:

```text
/sys/fs/cgroup/containerlite
```

The configured limits can be inspected from the host:

```bash
sudo cat /sys/fs/cgroup/containerlite/memory.max
sudo cat /sys/fs/cgroup/containerlite/pids.max
sudo cat /sys/fs/cgroup/containerlite/cpu.max
```

When the container exits, the cgroup is removed.

---

## Resource Isolation

ContainerLite uses cgroups v2 to restrict resource usage.

### Memory

The memory limit is configured through:

```text
memory.max
```

### CPU

CPU usage is controlled through:

```text
cpu.max
```

### Processes

The maximum number of processes is controlled through:

```text
pids.max
```

For example, attempting to create more processes than the configured limit results in:

```text
can't fork: Resource temporarily unavailable
```

This demonstrates that the process limit is being enforced by the kernel.

---

## Cleanup

ContainerLite cleans up resources after the container exits.

The following resources are removed:

* Container cgroup
* Host-side veth interface
* Container networking resources

Cleanup is performed even when the container process exits unexpectedly through the runtime's cleanup logic.

---

## Example

Run:

```bash
sudo python3 -m containerlite --memory 100M --pids 20 -- /bin/sh
```

Inside the container:

```bash
hostname
```

```text
containerlite
```

Check the PID:

```bash
echo $$
```

```text
1
```

Check networking:

```bash
ip addr
```

Test the host connection:

```bash
ping -c 3 10.0.0.1
```

Then exit:

```bash
exit
```

ContainerLite cleans up the associated resources automatically.

---

## Technologies Used

* **Python**
* **Linux Namespaces**
* **Linux cgroups v2**
* **chroot**
* **BusyBox**
* **veth**
* **Linux networking**
* **subprocess / `unshare`**

---

## What I Learned

This project was built to understand how container runtimes work at the Linux kernel level.

Key concepts explored:

* Process isolation with PID namespaces
* Filesystem isolation with mount namespaces and `chroot`
* Hostname isolation with UTS namespaces
* Network isolation with network namespaces
* Virtual Ethernet networking
* Linux cgroups v2
* CPU, memory, and process resource limits
* Linux `/proc`
* Process lifecycle and exit-code propagation
* Cleanup of kernel resources

---

## Limitations

ContainerLite is intentionally minimal.

It currently does not attempt to provide the full feature set of production container runtimes.

Examples of features outside the current scope include:

* Image management
* Container registries
* Advanced DNS configuration
* Production-grade security isolation

---

