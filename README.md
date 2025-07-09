# NetThrottle

A modern, cross-platform GUI application built with Python tkinter to monitor network speeds and control bandwidth on supported systems.

## Features

- **Cross-Platform Support**: Works on both Windows and Linux
- **Modern GUI Interface**: Clean, responsive design with dark/light themes
- **Real-time Network Monitoring**: Monitor current network speeds across all platforms
- **Bandwidth Control (Linux Only)**: Limit download and upload speeds using traffic control (tc)
- **Multiple Network Interfaces**: Support for WiFi, Ethernet, and other interfaces
- **Flexible Speed Units**: Set limits in Kbps or Mbps
- **Status Logging**: View network statistics and system information
- **Always Maximized**: Professional full-screen interface

## Platform Support

### ✅ Windows
- ✅ Network monitoring and statistics
- ✅ Interface detection and selection
- ✅ Real-time speed monitoring
- ❌ Bandwidth limiting (not supported by Windows API)

### ✅ Linux  
- ✅ Full network monitoring and statistics
- ✅ Interface detection and selection
- ✅ Real-time speed monitoring
- ✅ Download/Upload bandwidth limiting via traffic control (tc)

## Requirements

### Windows
- Python 3.12 or higher
- Administrative privileges (recommended)

### Linux
- Python 3.12 or higher
- Root/sudo privileges (required for bandwidth control)
- iproute2 package (usually pre-installed)

## Installation

### Quick Setup (Cross-Platform)
```bash
# Make setup script executable (Linux/macOS)
chmod +x setup.sh && ./setup.sh

# Or use cross-platform launcher
chmod +x run_cross_platform.sh
```

### Windows Setup
```batch
# Option 1: Use the Windows batch file
run_windows.bat

# Option 2: Direct Python execution
python main.py
```

### Linux Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install traffic control utilities (if not already installed)
sudo apt-get install iproute2  # Ubuntu/Debian
# or
sudo yum install iproute       # CentOS/RHEL
# or
sudo pacman -S iproute2        # Arch Linux

# Load ifb module for upload limiting
sudo modprobe ifb
```

## Usage

### Quick Start (Cross-Platform)
```bash
# Cross-platform launcher
./run_cross_platform.sh

# Windows
run_windows.bat

# Linux with bandwidth control
sudo python3 main.py
```

### Running the Application

#### Windows
```batch
# Option 1: Use provided batch file
run_windows.bat

# Option 2: Direct execution
python main.py
```

#### Linux
```bash
# Full functionality (bandwidth control + monitoring)
sudo python3 main.py

# Monitoring only (without bandwidth control)
python3 main.py
```

#### Cross-Platform
```bash
# Auto-detect platform and run appropriately
./run_cross_platform.sh
```

### Using the Application

1. **Network Interface Selection**: 
   - The application auto-detects available network interfaces
   - Select your active interface from the dropdown (e.g., "Wi-Fi" on Windows, "wlan0" on Linux)

2. **Setting Speed Limits** (Linux Only):
   - Enter desired speed value in the input field
   - Select unit (kbps or mbps) from dropdown
   - Click "Set Download Limit" or "Set Upload Limit"
   - **Note**: Requires sudo privileges on Linux

3. **Network Monitoring** (All Platforms):
   - Real-time speed monitoring in the main dashboard
   - Live statistics cards showing current speeds
   - Network interface statistics and information

4. **Remove Limits** (Linux Only): 
   - Click "Remove All Limits" to clear all bandwidth restrictions

### Example Speed Limits
- **1 Mbps** = Basic web browsing
- **5 Mbps** = Standard definition video streaming
- **25 Mbps** = High definition video streaming
- **100 Mbps** = High-speed downloads and 4K streaming

### Platform-Specific Notes

#### Windows Users
- Application provides full network monitoring capabilities
- Bandwidth limiting is not supported due to Windows API limitations
- Administrative privileges recommended for optimal performance
- Interface names typically appear as "Wi-Fi", "Ethernet", "Local Area Connection"

#### Linux Users
- Full bandwidth control using Traffic Control (tc)
- Requires sudo privileges for bandwidth modification
- Interface names typically appear as "wlan0", "eth0", "enp0s3"
- Uses HTB and IFB for precise traffic shaping

## How It Works

### Cross-Platform Network Monitoring
- **psutil Library**: Cross-platform network interface detection and statistics
- **Real-time Updates**: Live monitoring of bytes sent/received across all supported platforms
- **Interface Detection**: Automatic discovery of active network interfaces

### Linux Bandwidth Control
- **Download Limiting**: HTB (Hierarchical Token Bucket) queueing discipline
- **Upload Limiting**: IFB (Intermediate Functional Block) devices for traffic redirection
- **Traffic Shaping**: Precise control using Linux kernel's traffic control subsystem

## Technical Details

### Traffic Control Commands Used
The application executes these types of commands:

```bash
# Download limiting
sudo tc qdisc add dev wlan0 root handle 1: htb default 30
sudo tc class add dev wlan0 parent 1: classid 1:1 htb rate 1000kbit
sudo tc class add dev wlan0 parent 1:1 classid 1:10 htb rate 1000kbit ceil 1000kbit

# Upload limiting (more complex)
sudo tc qdisc add dev wlan0 ingress
sudo tc filter add dev wlan0 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0
```

### Network Interfaces
The application automatically detects available network interfaces and filters out:
- Loopback interfaces (lo)
- Inactive interfaces
- Virtual interfaces without IP addresses

## Troubleshooting

### Permission Issues
```bash
# If you get permission errors, run with sudo
sudo python main.py
```

### Interface Not Found
```bash
# List available interfaces
ip link show

# or
ifconfig
```

### Traffic Control Not Working
```bash
# Check if tc is installed
which tc

# Install if missing
sudo apt-get install iproute2
```

### IFB Module Issues
```bash
# Load ifb module manually
sudo modprobe ifb

# Check if loaded
lsmod | grep ifb
```

## Limitations

- **Linux Only**: This application only works on Linux systems
- **Root Required**: Requires sudo/root privileges to modify network settings
- **Interface Specific**: Speed limits apply per network interface
- **System Wide**: Affects all applications using the selected interface

## Safety Notes

- Speed limits persist until removed or system restart
- Always test with conservative limits first
- Remove limits before troubleshooting network issues
- Keep terminal access available in case GUI becomes unresponsive

## File Structure

```
speed_limiter/
├── main.py                    # Main application
├── requirements.txt           # Python dependencies
├── setup.sh                  # Setup script
├── pyproject.toml            # Project configuration
├── README.md                 # This file
└── speed_limiter_settings.json  # Settings (created on first run)
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source. Use at your own risk.

## Disclaimer

This tool modifies system network settings. Use responsibly and ensure you understand the implications of bandwidth limiting on your system.
