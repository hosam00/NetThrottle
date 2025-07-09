#!/bin/bash

# Check the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Starting NetThrottle on Linux..."
    echo "Note: Bandwidth limiting requires sudo privileges"
    echo ""
    python3 main.py
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Starting NetThrottle on Windows..."
    echo "Note: Administrator privileges recommended"
    echo ""
    python main.py
else
    echo "Starting NetThrottle..."
    python3 main.py || python main.py
fi
