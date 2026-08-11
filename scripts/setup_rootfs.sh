#!/bin/bash

set -e

ROOTFS="rootfs"

echo "[ContainerLite] Setting up rootfs..."

rm -rf "$ROOTFS"

mkdir -p "$ROOTFS/bin"
mkdir -p "$ROOTFS/proc"
mkdir -p "$ROOTFS/tmp"

if [ ! -f /usr/bin/busybox ]; then
    echo "Error: /usr/bin/busybox not found"
    echo "Install it with: sudo apt install busybox-static"
    exit 1
fi

cp /usr/bin/busybox "$ROOTFS/bin/busybox"

cd "$ROOTFS/bin"

for cmd in $(./busybox --list); do
    [ "$cmd" = "busybox" ] && continue
    ln -s busybox "$cmd"
done

echo "[ContainerLite] rootfs ready."
