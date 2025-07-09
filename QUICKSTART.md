# 🚀 Quick Start Guide

## Modern Network Speed Controller

### Installation & Setup
```bash
# Option 1: Automated setup
./setup.sh

# Option 2: Manual setup
sudo apt-get install python3-psutil iproute2
sudo modprobe ifb
```

### Running the Application
```bash
# With modern launcher
./run.sh

# With full privileges (recommended)
sudo ./run.sh

# Direct launch
python3 main.py
```

### Modern Features
- **🎨 Dark Theme**: Modern dark UI with card-based layout
- **🔔 Smart Notifications**: Custom notification system instead of basic popups
- **📊 Real-time Monitoring**: Live speed monitoring with formatted display
- **⚡ Quick Actions**: One-click speed limiting and removal
- **💾 Settings Persistence**: Automatically saves your preferences
- **🎯 Intuitive Interface**: Clean, modern interface with icons

### Speed Control Examples
- **Light browsing**: 1-5 Mbps
- **Video streaming**: 10-25 Mbps  
- **Gaming**: 50-100 Mbps
- **Downloads**: 500+ Mbps

### Keyboard Shortcuts
- **Ctrl+R**: Refresh status
- **Ctrl+Q**: Quit application
- **Ctrl+S**: Save settings

### Tips for Best Results
1. **Run with sudo** for full traffic control functionality
2. **Select correct interface** (wlan0 for WiFi, eth0 for Ethernet)
3. **Test with conservative limits** first
4. **Monitor real-time speeds** in the status panel
5. **Remove limits** when done to restore full speed

### Troubleshooting
- **Permission errors**: Run with `sudo ./run.sh`
- **Interface not found**: Check available interfaces with `ip link`
- **Commands fail**: Ensure `iproute2` package is installed
- **Upload limiting issues**: Verify `ifb` module is loaded

### Modern Design Elements
- **Card-based layout** for better organization
- **Color-coded status messages** for quick recognition
- **Responsive design** that adapts to window size
- **Modern typography** with Segoe UI font
- **Interactive notifications** with auto-dismiss
- **Professional color scheme** with accent colors

## 📱 Responsive Design Features

### Window Management
- **Auto-sizing**: Window automatically adjusts to your screen size
- **Minimum size**: 650x600 pixels to ensure all controls are visible
- **Centered positioning**: Window opens centered on your screen
- **Scrollable interface**: If content doesn't fit, scroll to access all features

### Keyboard Shortcuts
- **F11**: Toggle fullscreen/maximize
- **Ctrl+R**: Refresh network status
- **Ctrl+S**: Save current settings
- **Ctrl+Q** or **Escape**: Quit application

### Responsive Layout
- **Cards auto-stack**: Interface components adapt to window width
- **Scrolling support**: Mouse wheel scrolling when content overflows
- **Flexible controls**: Input fields and buttons adjust to available space
- **Status panel**: Always visible with appropriate height

### Troubleshooting Display Issues
```bash
# If the window is too small
# Press F11 to maximize or resize the window manually

# If you can't see the status panel
# Try scrolling down or maximizing the window

# For very small screens
# The interface will become scrollable automatically
```
