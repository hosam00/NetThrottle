# 🌐 NetThrottle

> **Modern Cross-Platform Network Speed Monitoring & Bandwidth Control**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/netthrottle)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

NetThrottle is a modern, professional GUI application that provides real-time network monitoring and intelligent bandwidth control across Windows and Linux platforms.

## ✨ Features

### 🖥️ Cross-Platform Support
- **Windows**: Full network monitoring with beautiful interface
- **Linux**: Complete bandwidth control + monitoring capabilities

### 🎯 Core Capabilities
- **Real-time Network Monitoring** - Live speed tracking across all interfaces
- **Bandwidth Limiting** (Linux) - Precise download/upload speed control
- **Interface Detection** - Auto-discovery of all network connections
- **Modern GUI** - Clean, responsive design that always opens maximized
- **Smart Notifications** - Context-aware alerts and status updates

### 🔧 Technical Features
- **Traffic Control Integration** (Linux) - Uses kernel-level `tc` for precise control
- **Cross-Platform Interface Detection** - Works with WiFi, Ethernet, and more
- **Real-time Statistics** - Live byte counters and speed calculations
- **Settings Persistence** - Remembers your preferences
- **Keyboard Shortcuts** - Quick access to common functions

## 🚀 Quick Start

### Windows Users
```batch
# Download and run
git clone https://github.com/yourusername/netthrottle.git
cd netthrottle
setup_windows.bat
run_windows.bat
```

### Linux Users
```bash
# Download and run
git clone https://github.com/yourusername/netthrottle.git
cd netthrottle
chmod +x setup.sh && ./setup.sh
sudo python3 main.py  # Full features
```

### Universal Launcher
```bash
# Auto-detects your platform
./run_cross_platform.sh
```

## 📊 Platform Compatibility

| Feature | Windows | Linux |
|---------|:-------:|:-----:|
| Network Monitoring | ✅ | ✅ |
| Real-time Statistics | ✅ | ✅ |
| Interface Detection | ✅ | ✅ |
| Modern GUI | ✅ | ✅ |
| Download Limiting | ❌ | ✅ |
| Upload Limiting | ❌ | ✅ |

## 🎨 Screenshots

*Coming soon - showcasing the modern interface on both platforms*

## 🛠️ Installation

### Requirements
- **Python 3.12+** (all platforms)
- **Administrator/sudo privileges** (recommended)
- **iproute2** (Linux only, usually pre-installed)

### Dependencies
```bash
pip install psutil
```

See [CROSS_PLATFORM_GUIDE.md](CROSS_PLATFORM_GUIDE.md) for detailed platform-specific instructions.

## 💡 Usage Examples

### Basic Monitoring (All Platforms)
1. Launch NetThrottle
2. Select your network interface
3. View real-time speeds in the dashboard

### Bandwidth Control (Linux Only)
1. Run with sudo: `sudo python3 main.py`
2. Set download limit: Enter speed + unit, click "Set Download Limit"
3. Set upload limit: Enter speed + unit, click "Set Upload Limit"
4. Remove limits: Click "Remove All Limits"

### Speed Examples
- **1 Mbps** - Basic web browsing
- **5 Mbps** - SD video streaming
- **25 Mbps** - HD video streaming
- **100 Mbps** - 4K streaming, large downloads

## ⌨️ Keyboard Shortcuts

- `Ctrl+R` - Refresh network status
- `Ctrl+S` - Save current settings
- `Ctrl+Q` - Quit application
- `Escape` - Close application

## 🔧 Technical Details

### Linux Bandwidth Control
- **Download Limiting**: HTB (Hierarchical Token Bucket) queueing
- **Upload Limiting**: IFB (Intermediate Functional Block) redirection
- **Precision**: Kernel-level traffic shaping for accurate control

### Cross-Platform Monitoring
- **Interface Detection**: `psutil.net_if_addrs()` for universal compatibility
- **Statistics**: Real-time byte counting and speed calculations
- **GUI Framework**: tkinter with modern styling

## 📚 Documentation

- [Cross-Platform Guide](CROSS_PLATFORM_GUIDE.md) - Detailed platform instructions
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [Quick Start Guide](QUICKSTART.md) - Get up and running fast

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Why NetThrottle?

- **Professional Grade**: Built with enterprise-quality code and modern design
- **Cross-Platform**: One application that works seamlessly on multiple operating systems
- **User-Friendly**: Intuitive interface that doesn't require networking expertise
- **Powerful**: Kernel-level traffic control where supported, with graceful degradation
- **Modern**: Always-maximized interface with responsive design and real-time updates

---

**Made with ❤️ for network administrators, developers, and power users who need precise network control.**
