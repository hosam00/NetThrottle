#!/bin/bash

# Network Speed Controller Setup Script

echo "Setting up Network Speed Controller..."

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "This application is designed for Linux systems only."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if tc (traffic control) is available
if ! command -v tc &> /dev/null; then
    echo "Installing traffic control utilities..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y iproute2
    elif command -v yum &> /dev/null; then
        sudo yum install -y iproute
    elif command -v pacman &> /dev/null; then
        sudo pacman -S iproute2
    else
        echo "Please install iproute2 package manually for your distribution."
        exit 1
    fi
fi

# Load ifb module (needed for upload limiting)
echo "Loading ifb kernel module..."
sudo modprobe ifb

# Add ifb to modules to load at boot
if ! grep -q "ifb" /etc/modules 2>/dev/null; then
    echo "ifb" | sudo tee -a /etc/modules
fi

echo "Setup complete!"
echo ""
echo "Usage:"
echo "  python main.py"
echo ""
echo "Note: The application requires sudo privileges to modify network settings."
echo "You may need to run it with: sudo python main.py"
