#!/usr/bin/env bash

set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Please run this script with sudo (required for system packages)." >&2
  exit 1
fi

apt-get update
apt-get install -y \
  python3 \
  python3-dev \
  python3-pip \
  ipython3 \
  bluetooth \
  libbluetooth-dev \
  bluez \
  bluez-tools \
  blueman

python3 -m pip install --upgrade pip
python3 -m pip install pybluez pytest

echo "Dependencies installed. You can now run run_server.py and run_client.py"

