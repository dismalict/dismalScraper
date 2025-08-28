#!/bin/bash

# ===============================
# Install dependencies for Python script
# ===============================

# Exit on error
set -e

# Check if running as root (optional)
if [ "$EUID" -ne 0 ]; then
  echo "Warning: Not running as root. Some commands may require sudo."
fi

echo "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-venv python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-venv python3-pip
    else
        echo "Unsupported package manager. Install Python 3 manually."
        exit 1
    fi
else
    echo "Python 3 found: $(python3 --version)"
fi

echo "Checking for pip..."
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py
    rm get-pip.py
else
    echo "pip3 found: $(pip3 --version)"
fi

echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install requests

echo "All dependencies installed successfully."
