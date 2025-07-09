# Cross-Platform Guide - NetThrottle

This guide provides detailed instructions for running NetThrottle on both Windows and Linux platforms.

## Platform Compatibility Matrix

| Feature | Windows | Linux |
|---------|---------|-------|
| Network Monitoring | ✅ Full Support | ✅ Full Support |
| Interface Detection | ✅ Full Support | ✅ Full Support |
| Real-time Statistics | ✅ Full Support | ✅ Full Support |
| GUI Interface | ✅ Full Support | ✅ Full Support |
| Download Speed Limiting | ❌ Not Supported | ✅ Full Support |
| Upload Speed Limiting | ❌ Not Supported | ✅ Full Support |

## Windows Installation & Usage

### Prerequisites
- Windows 10/11 (recommended)
- Python 3.12 or higher
- Administrator privileges (recommended)

### Installation Steps

1. **Install Python** (if not already installed):
   - Download from https://python.org
   - **Important**: Check "Add Python to PATH" during installation

2. **Download the Application**:
   - Clone or download this repository
   - Extract to your desired location

3. **Run Setup**:
   ```batch
   # Double-click or run from command prompt
   setup_windows.bat
   ```

4. **Start the Application**:
   ```batch
   # Double-click or run from command prompt
   run_windows.bat
   ```

### Windows-Specific Features

- **Network Interfaces**: Displays as "Wi-Fi", "Ethernet", "Local Area Connection"
- **Monitoring Only**: Bandwidth limiting controls will show "Not Supported" warnings
- **Real-time Stats**: Full network monitoring capabilities available
- **Admin Privileges**: Recommended for accessing all network information

### Windows Limitations

The Windows version does not support bandwidth limiting because:
- Windows doesn't have built-in traffic control like Linux's `tc`
- Third-party solutions require kernel-level access
- Windows API doesn't provide user-space bandwidth control

### Windows Troubleshooting

**Python Not Found Error**:
```
'python' is not recognized as an internal or external command
```
- Reinstall Python with "Add Python to PATH" checked
- Or use full path: `C:\Python312\python.exe main.py`

**Permission Issues**:
- Right-click Command Prompt and select "Run as Administrator"
- Or right-click the .bat file and select "Run as Administrator"

## Linux Installation & Usage

### Prerequisites
- Any modern Linux distribution
- Python 3.12 or higher
- Root/sudo privileges (for bandwidth control)
- iproute2 package (usually pre-installed)

### Installation Steps

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd speed_limiter
   ```

2. **Run Setup**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start Application**:
   ```bash
   # Full functionality (requires sudo)
   sudo python3 main.py
   
   # Monitoring only
   python3 main.py
   ```

### Linux-Specific Features

- **Network Interfaces**: Displays as "wlan0", "eth0", "enp0s3", etc.
- **Full Bandwidth Control**: Download and upload limiting available
- **Traffic Control**: Uses Linux kernel's `tc` (traffic control) system
- **Real-time Monitoring**: Complete network statistics and control

### Linux Bandwidth Control Details

**Download Limiting**:
- Uses HTB (Hierarchical Token Bucket) queueing discipline
- Applied to the root qdisc of the interface
- Precise rate limiting with burst handling

**Upload Limiting**:
- Uses IFB (Intermediate Functional Block) devices
- Redirects ingress traffic for egress shaping
- More complex but provides accurate upload control

### Linux Troubleshooting

**Permission Denied**:
```bash
# Make sure to run with sudo for bandwidth control
sudo python3 main.py
```

**Traffic Control Not Found**:
```bash
# Install iproute2 package
sudo apt install iproute2      # Ubuntu/Debian
sudo yum install iproute        # CentOS/RHEL  
sudo pacman -S iproute2         # Arch Linux
```

**Module Loading Issues**:
```bash
# Load required kernel modules
sudo modprobe ifb
sudo modprobe sch_htb
```

## Cross-Platform Usage Guide

### Starting the Application

**Cross-Platform Launcher**:
```bash
./run_cross_platform.sh
```

**Platform-Specific**:
```bash
# Windows
run_windows.bat

# Linux (full features)
sudo python3 main.py

# Linux (monitoring only)
python3 main.py
```

### Interface Usage

1. **Network Interface Selection**:
   - Automatically detects available interfaces
   - Select your active connection from dropdown
   - Interface names vary by platform

2. **Network Monitoring** (All Platforms):
   - Real-time speed display in statistics cards
   - Live network activity in the monitoring panel
   - Interface statistics and byte counters

3. **Bandwidth Control** (Linux Only):
   - Enter speed limit in input field
   - Select unit (kbps/mbps)
   - Click "Set Download/Upload Limit"
   - Use "Remove All Limits" to clear restrictions

### Keyboard Shortcuts (All Platforms)

- `Ctrl+R`: Refresh network status
- `Ctrl+S`: Save current settings
- `Ctrl+Q`: Quit application
- `Escape`: Close application

## Development Notes

### Platform Detection
The application automatically detects the operating system using:
```python
import platform
os_type = platform.system().lower()
is_windows = os_type == 'windows'
is_linux = os_type == 'linux'
```

### Window Maximization
- **Windows**: Uses `root.state('zoomed')`
- **Linux**: Uses `root.attributes('-zoomed', True)`
- **Fallback**: Manual geometry setting for other platforms

### Network Interface Detection
Uses `psutil.net_if_addrs()` for cross-platform interface discovery with platform-specific filtering and naming conventions.

## Support & Troubleshooting

### Common Issues

**Application Won't Start**:
1. Check Python installation
2. Verify required packages are installed
3. Try running from command line to see error messages

**No Network Interfaces Found**:
1. Check network connections are active
2. Verify psutil package is installed correctly
3. Try refreshing the interface list

**Bandwidth Control Not Working (Linux)**:
1. Ensure running with sudo privileges
2. Check if tc (traffic control) is installed
3. Verify interface name is correct

### Getting Help

For additional support:
1. Check error messages in the application log
2. Verify system requirements are met
3. Consult platform-specific documentation
4. Open an issue with detailed error information

## Security Considerations

### Windows
- Application requests minimal system access
- No kernel-level modifications
- Safe to run with standard user privileges

### Linux
- Requires root privileges for traffic control
- Modifies kernel network stack temporarily
- Changes are non-persistent (removed on reboot)
- No permanent system modifications

Both platforms handle network monitoring safely through the psutil library without requiring special privileges for basic functionality.
