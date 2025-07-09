import tkinter as tk
from tkinter import ttk, messagebox, font
import subprocess
import threading
import time
import re
import psutil
import json
import os
import platform
import sys

class NetworkSpeedController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NetThrottle - Network Speed Controller")
        
        # Detect operating system for cross-platform compatibility
        self.os_type = platform.system().lower()
        self.is_windows = self.os_type == 'windows'
        self.is_linux = self.os_type == 'linux'
        
        # Cross-platform window maximization
        self.maximize_window()
        self.root.minsize(800, 600)
        
        # Modern styling
        self.setup_modern_theme()
        self.root.configure(bg='#f5f5f5')  # Light modern background
        
        # Variables
        self.current_download_limit = tk.StringVar(value="No limit")
        self.current_upload_limit = tk.StringVar(value="No limit")
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Get network interfaces
        self.interfaces = self.get_network_interfaces()
        self.selected_interface = tk.StringVar(value=self.interfaces[0] if self.interfaces else "")
        
        # Modern colors - Clean light theme
        self.colors = {
            'bg': '#f5f5f5',
            'card_bg': '#ffffff',
            'accent': '#2563eb',
            'accent_hover': '#1d4ed8',
            'success': '#059669',
            'warning': '#d97706',
            'danger': '#dc2626',
            'text': '#1f2937',
            'text_secondary': '#6b7280',
            'border': '#e5e7eb',
            'hover': '#f3f4f6'
        }
        
        self.setup_ui()
        self.load_settings()
        
    def maximize_window(self):
        """Cross-platform window maximization"""
        try:
            if self.is_windows:
                # Windows maximization
                self.root.state('zoomed')
            elif self.is_linux:
                # Linux maximization
                self.root.attributes('-zoomed', True)
            else:
                # Fallback for other platforms
                self.root.geometry("1200x800")
                
        except Exception as e:
            # Fallback if maximization fails
            self.root.geometry("1200x800")
            print(f"Warning: Could not maximize window: {e}")
    
    def check_platform_support(self):
        """Check and display platform-specific feature support"""
        if self.is_windows:
            self.show_modern_notification(
                "Platform Info", 
                "Running on Windows. Bandwidth limiting is not supported on this platform.", 
                "warning"
            )
        elif self.is_linux:
            # Check if tc is available
            try:
                result = subprocess.run("which tc", shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    self.show_modern_notification(
                        "Missing Dependency", 
                        "Traffic Control (tc) not found. Install with: sudo apt install iproute2", 
                        "warning"
                    )
            except:
                pass

    def setup_modern_theme(self):
        """Setup clean modern light theme for ttk widgets"""
        style = ttk.Style()
        
        # Use a clean modern theme
        style.theme_use('clam')
        
        # Configure clean modern styles
        style.configure('Card.TFrame',
                       background='#ffffff',
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Modern.TLabel',
                       background='#ffffff',
                       foreground='#1f2937',
                       font=('Inter', 11))
        
        style.configure('Title.TLabel',
                       background='#f5f5f5',
                       foreground='#111827',
                       font=('Inter', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background='#ffffff',
                       foreground='#111827',
                       font=('Inter', 14, 'bold'))
        
        style.configure('Status.TLabel',
                       background='#f5f5f5',
                       foreground='#6b7280',
                       font=('Inter', 10))
        
        style.configure('Info.TLabel',
                       background='#ffffff',
                       foreground='#6b7280',
                       font=('Inter', 10))
        
        style.configure('Modern.TEntry',
                       fieldbackground='#f9fafb',
                       foreground='#1f2937',
                       bordercolor='#d1d5db',
                       lightcolor='#2563eb',
                       darkcolor='#2563eb',
                       borderwidth=2,
                       insertcolor='#1f2937',
                       relief='flat')
        
        style.configure('Modern.TCombobox',
                       fieldbackground='#f9fafb',
                       foreground='#1f2937',
                       bordercolor='#d1d5db',
                       lightcolor='#2563eb',
                       darkcolor='#2563eb',
                       borderwidth=2,
                       arrowcolor='#6b7280',
                       relief='flat')
        
        style.configure('Primary.TButton',
                       background='#2563eb',
                       foreground='#ffffff',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Inter', 10, 'bold'),
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', '#1d4ed8'),
                           ('pressed', '#1e40af')])
        
        style.configure('Success.TButton',
                       background='#059669',
                       foreground='#ffffff',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Inter', 10, 'bold'),
                       relief='flat')
        
        style.map('Success.TButton',
                 background=[('active', '#047857'),
                           ('pressed', '#065f46')])
        
        style.configure('Danger.TButton',
                       background='#dc2626',
                       foreground='#ffffff',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Inter', 10, 'bold'),
                       relief='flat')
        
        style.map('Danger.TButton',
                 background=[('active', '#b91c1c'),
                           ('pressed', '#991b1b')])
        
    def get_network_interfaces(self):
        """Get available network interfaces (cross-platform)"""
        try:
            interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                # Skip loopback interfaces
                if interface.lower() in ['lo', 'loopback']:
                    continue
                    
                # Check if interface has an IP address
                if any(addr.family == 2 for addr in addrs):  # AF_INET = 2
                    interfaces.append(interface)
            
            # Return found interfaces or platform-specific defaults
            if interfaces:
                return interfaces
            elif self.is_windows:
                return ['Wi-Fi', 'Ethernet', 'Local Area Connection']
            else:
                return ['eth0', 'wlan0', 'enp0s3']
                
        except Exception:
            # Fallback defaults based on platform
            if self.is_windows:
                return ['Wi-Fi', 'Ethernet', 'Local Area Connection']
            else:
                return ['eth0', 'wlan0', 'enp0s3']
    
    def setup_ui(self):
        """Setup clean, modern user interface"""
        # Configure root for proper resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container with sidebar layout
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure main container
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Left sidebar
        sidebar = tk.Frame(main_container, bg='#ffffff', width=300)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        sidebar.grid_propagate(False)
        
        # Main content area
        content_area = tk.Frame(main_container, bg=self.colors['bg'])
        content_area.grid(row=0, column=1, sticky="nsew")
        
        # Setup sidebar
        self.setup_sidebar(sidebar)
        
        # Setup main content
        self.setup_main_content(content_area)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-r>', lambda e: self.refresh_status())
        self.root.bind('<Control-s>', lambda e: self.save_settings())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Escape>', lambda e: self.on_closing())
        
        # Start monitoring
        self.start_monitoring()
        
        # Check platform support and show warnings if needed
        self.root.after(1000, self.check_platform_support)  # Delay to let UI load first
    
    def setup_sidebar(self, parent):
        """Setup the left sidebar with controls"""
        # Header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill=tk.X, padx=30, pady=(40, 30))
        
        title_label = ttk.Label(header_frame, text="NetThrottle", 
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Network Speed Controller", 
                                 style='Status.TLabel')
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Interface Selection
        interface_section = tk.Frame(parent, bg='#ffffff')
        interface_section.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        ttk.Label(interface_section, text="Network Interface", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        interface_combo = ttk.Combobox(interface_section, textvariable=self.selected_interface, 
                                     values=self.interfaces, state="readonly", 
                                     style='Modern.TCombobox', font=('Inter', 11))
        interface_combo.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(interface_section, text="Select your active network interface", 
                 style='Info.TLabel').pack(anchor=tk.W)
        
        # Download Control
        download_section = tk.Frame(parent, bg='#ffffff')
        download_section.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        ttk.Label(download_section, text="Download Limit", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        download_input_frame = tk.Frame(download_section, bg='#ffffff')
        download_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.download_entry = ttk.Entry(download_input_frame, style='Modern.TEntry', 
                                       font=('Inter', 11))
        self.download_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.download_unit = ttk.Combobox(download_input_frame, values=["kbps", "mbps"], 
                                        state="readonly", width=8, style='Modern.TCombobox',
                                        font=('Inter', 11))
        self.download_unit.set("mbps")
        self.download_unit.pack(side=tk.RIGHT)
        
        ttk.Button(download_section, text="Set Download Limit", 
                  command=self.set_download_limit, 
                  style='Primary.TButton').pack(fill=tk.X, pady=(0, 10))
        
        # Current download limit display
        download_status_frame = tk.Frame(download_section, bg='#f8fafc', relief='flat')
        download_status_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(download_status_frame, text="Current: ", 
                 style='Info.TLabel').pack(side=tk.LEFT, padx=10, pady=8)
        ttk.Label(download_status_frame, textvariable=self.current_download_limit, 
                 style='Modern.TLabel').pack(side=tk.LEFT, pady=8)
        
        # Upload Control
        upload_section = tk.Frame(parent, bg='#ffffff')
        upload_section.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        ttk.Label(upload_section, text="Upload Limit", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        upload_input_frame = tk.Frame(upload_section, bg='#ffffff')
        upload_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.upload_entry = ttk.Entry(upload_input_frame, style='Modern.TEntry',
                                     font=('Inter', 11))
        self.upload_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.upload_unit = ttk.Combobox(upload_input_frame, values=["kbps", "mbps"], 
                                      state="readonly", width=8, style='Modern.TCombobox',
                                      font=('Inter', 11))
        self.upload_unit.set("mbps")
        self.upload_unit.pack(side=tk.RIGHT)
        
        ttk.Button(upload_section, text="Set Upload Limit", 
                  command=self.set_upload_limit, 
                  style='Primary.TButton').pack(fill=tk.X, pady=(0, 10))
        
        # Current upload limit display
        upload_status_frame = tk.Frame(upload_section, bg='#f8fafc', relief='flat')
        upload_status_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(upload_status_frame, text="Current: ", 
                 style='Info.TLabel').pack(side=tk.LEFT, padx=10, pady=8)
        ttk.Label(upload_status_frame, textvariable=self.current_upload_limit, 
                 style='Modern.TLabel').pack(side=tk.LEFT, pady=8)
        
        # Action Buttons
        actions_section = tk.Frame(parent, bg='#ffffff')
        actions_section.pack(fill=tk.X, padx=30, pady=(0, 40))
        
        ttk.Button(actions_section, text="Remove All Limits", 
                  command=self.remove_all_limits, 
                  style='Danger.TButton').pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(actions_section, text="Save Settings", 
                  command=self.save_settings, 
                  style='Success.TButton').pack(fill=tk.X)
    
    def setup_main_content(self, parent):
        """Setup the main content area with status and monitoring"""
        # Configure content area
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Top stats cards
        stats_frame = tk.Frame(parent, bg=self.colors['bg'])
        stats_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=30)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Stats cards
        self.create_stat_card(stats_frame, "Network Status", "🌐", "Active", 0)
        self.create_stat_card(stats_frame, "Download Speed", "📥", "Monitoring...", 1)
        self.create_stat_card(stats_frame, "Upload Speed", "📤", "Monitoring...", 2)
        
        # Status monitor area
        monitor_frame = tk.Frame(parent, bg='#ffffff', relief='flat')
        monitor_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 30))
        
        # Monitor header
        monitor_header = tk.Frame(monitor_frame, bg='#ffffff')
        monitor_header.pack(fill=tk.X, padx=30, pady=(20, 10))
        
        ttk.Label(monitor_header, text="Real-time Network Monitor", 
                 style='Subtitle.TLabel').pack(side=tk.LEFT)
        
        ttk.Button(monitor_header, text="Refresh", 
                  command=self.refresh_status, 
                  style='Primary.TButton').pack(side=tk.RIGHT)
        
        # Monitor content
        monitor_content = tk.Frame(monitor_frame, bg='#ffffff')
        monitor_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.status_text = tk.Text(monitor_content, wrap=tk.WORD,
                                  bg='#f8fafc', fg=self.colors['text'], 
                                  insertbackground=self.colors['text'],
                                  selectbackground=self.colors['accent'],
                                  selectforeground='#ffffff',
                                  font=('JetBrains Mono', 10),
                                  border=0, relief='flat',
                                  padx=15, pady=15)
        
        status_scrollbar = ttk.Scrollbar(monitor_content, orient=tk.VERTICAL, 
                                       command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Welcome messages
        self.log_status("🚀 Network Speed Controller initialized successfully!")
        self.log_status(f"�️  Running on {platform.system()} ({platform.machine()})")
        
        if self.is_windows:
            self.log_status("💡 Windows detected - Network monitoring available")
            self.log_status("⚠️  Bandwidth limiting not supported on Windows")
        elif self.is_linux:
            self.log_status("💡 Linux detected - Full bandwidth control available")
            self.log_status("⚠️  Root privileges required for traffic control")
        
        self.log_status("⌨️  Shortcuts: Ctrl+R=Refresh, Ctrl+S=Save, Ctrl+Q=Quit")
    
    def create_stat_card(self, parent, title, icon, value, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg='#ffffff', relief='flat')
        card.grid(row=0, column=column, sticky="ew", padx=(0, 15) if column < 2 else (0, 0))
        
        card_content = tk.Frame(card, bg='#ffffff')
        card_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon and title
        header_frame = tk.Frame(card_content, bg='#ffffff')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        icon_label = tk.Label(header_frame, text=icon, font=('Inter', 16), 
                             bg='#ffffff', fg=self.colors['accent'])
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(header_frame, text=title, font=('Inter', 11, 'bold'), 
                              bg='#ffffff', fg=self.colors['text'])
        title_label.pack(side=tk.RIGHT)
        
        # Value
        value_label = tk.Label(card_content, text=value, font=('Inter', 14), 
                              bg='#ffffff', fg=self.colors['text_secondary'])
        value_label.pack(anchor=tk.W)
        
        # Store reference for updates
        if column == 1:
            self.download_stat_label = value_label
        elif column == 2:
            self.upload_stat_label = value_label
    def convert_to_kbps(self, value, unit):
        """Convert speed value to kbps"""
        try:
            value = float(value)
            if unit == "mbps":
                return int(value * 1000)
            return int(value)
        except ValueError:
            return None
    
    def set_download_limit(self):
        """Set download speed limit using tc (Linux only)"""
        # Check platform support
        if self.is_windows:
            self.show_modern_notification(
                "Not Supported", 
                "Bandwidth limiting is not supported on Windows. This feature requires Linux with Traffic Control (tc).", 
                "warning"
            )
            return
            
        speed = self.download_entry.get().strip()
        unit = self.download_unit.get()
        interface = self.selected_interface.get()
        
        if not speed or not interface:
            self.show_error_notification("Please enter speed and select interface")
            return
        
        speed_kbps = self.convert_to_kbps(speed, unit)
        if speed_kbps is None:
            self.show_error_notification("Invalid speed value")
            return
        
        try:
            # Remove existing rules
            subprocess.run(f"sudo tc qdisc del dev {interface} root", shell=True, 
                         stderr=subprocess.DEVNULL)
            
            # Add new download limit using HTB
            commands = [
                f"sudo tc qdisc add dev {interface} root handle 1: htb default 30",
                f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate {speed_kbps}kbit",
                f"sudo tc class add dev {interface} parent 1:1 classid 1:10 htb rate {speed_kbps}kbit ceil {speed_kbps}kbit"
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"Command failed: {cmd}\n{result.stderr}")
            
            self.current_download_limit.set(f"{speed} {unit}")
            self.log_status(f"✅ Download limit set to {speed} {unit}")
            self.show_modern_notification("Success!", f"Download limit set to {speed} {unit}", "success")
            
            # Update stat card
            if hasattr(self, 'download_stat_label'):
                self.download_stat_label.config(text=f"{speed} {unit}")
            
        except Exception as e:
            self.show_error_notification(f"Failed to set download limit: {str(e)}")
    
    def set_upload_limit(self):
        """Set upload speed limit using tc (Linux only)"""
        # Check platform support
        if self.is_windows:
            self.show_modern_notification(
                "Not Supported", 
                "Bandwidth limiting is not supported on Windows. This feature requires Linux with Traffic Control (tc).", 
                "warning"
            )
            return
            
        speed = self.upload_entry.get().strip()
        unit = self.upload_unit.get()
        interface = self.selected_interface.get()
        
        if not speed or not interface:
            self.show_error_notification("Please enter speed and select interface")
            return
        
        speed_kbps = self.convert_to_kbps(speed, unit)
        if speed_kbps is None:
            self.show_error_notification("Invalid speed value")
            return
        
        try:
            # Remove existing ingress rules
            subprocess.run(f"sudo tc qdisc del dev {interface} ingress", shell=True, 
                         stderr=subprocess.DEVNULL)
            
            # For upload limiting, we need to use ifb (Intermediate Functional Block)
            # This is more complex and requires additional setup
            self.setup_upload_limiting(interface, speed_kbps)
            
            self.current_upload_limit.set(f"{speed} {unit}")
            self.log_status(f"✅ Upload limit set to {speed} {unit}")
            self.show_modern_notification("Success!", f"Upload limit set to {speed} {unit}", "success")
            
            # Update stat card
            if hasattr(self, 'upload_stat_label'):
                self.upload_stat_label.config(text=f"{speed} {unit}")
            
        except Exception as e:
            self.show_error_notification(f"Failed to set upload limit: {str(e)}")
    
    def setup_upload_limiting(self, interface, speed_kbps):
        """Setup upload limiting using ifb"""
        try:
            # Load ifb module
            subprocess.run("sudo modprobe ifb", shell=True)
            
            # Create ifb interface
            subprocess.run("sudo ip link add ifb0 type ifb", shell=True, stderr=subprocess.DEVNULL)
            subprocess.run("sudo ip link set dev ifb0 up", shell=True)
            
            # Redirect ingress traffic to ifb0
            commands = [
                f"sudo tc qdisc add dev {interface} ingress",
                f"sudo tc filter add dev {interface} parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0",
                f"sudo tc qdisc add dev ifb0 root handle 1: htb default 30",
                f"sudo tc class add dev ifb0 parent 1: classid 1:1 htb rate {speed_kbps}kbit",
                f"sudo tc class add dev ifb0 parent 1:1 classid 1:10 htb rate {speed_kbps}kbit ceil {speed_kbps}kbit"
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0 and "File exists" not in result.stderr:
                    self.log_status(f"Warning: {cmd} - {result.stderr.strip()}")
                    
        except Exception as e:
            raise Exception(f"Upload limiting setup failed: {str(e)}")
    
    def remove_all_limits(self):
        """Remove all speed limits (Linux only)"""
        # Check platform support
        if self.is_windows:
            self.show_modern_notification(
                "Not Supported", 
                "Bandwidth limiting is not supported on Windows. This feature requires Linux with Traffic Control (tc).", 
                "warning"
            )
            return
            
        interface = self.selected_interface.get()
        if not interface:
            self.show_error_notification("Please select an interface")
            return
        
        try:
            # Remove all tc rules
            commands = [
                f"sudo tc qdisc del dev {interface} root",
                f"sudo tc qdisc del dev {interface} ingress",
                "sudo ip link del ifb0"
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
            
            self.current_download_limit.set("No limit")
            self.current_upload_limit.set("No limit")
            self.log_status("✅ All speed limits removed")
            self.show_modern_notification("Success!", "All speed limits removed", "success")
            
            # Update stat cards
            if hasattr(self, 'download_stat_label'):
                self.download_stat_label.config(text="No limit")
            if hasattr(self, 'upload_stat_label'):
                self.upload_stat_label.config(text="No limit")
            
        except Exception as e:
            self.show_error_notification(f"Failed to remove limits: {str(e)}")
    
    def refresh_status(self):
        """Refresh the current status (cross-platform)"""
        interface = self.selected_interface.get()
        if not interface:
            return
        
        try:
            # Platform-specific status checking
            if self.is_linux:
                # Check current tc rules on Linux
                result = subprocess.run(f"tc qdisc show dev {interface}", shell=True, 
                                      capture_output=True, text=True)
                
                self.log_status("=== Current Traffic Control Rules ===")
                if result.stdout.strip():
                    self.log_status(result.stdout)
                else:
                    self.log_status("No traffic control rules found")
            elif self.is_windows:
                # Windows status
                self.log_status("=== Windows Platform Status ===")
                self.log_status("Traffic control not supported on Windows")
                self.log_status("Monitoring network statistics only")
                
            # Check network statistics (works on all platforms)
            stats = psutil.net_io_counters(pernic=True)
            if interface in stats:
                stat = stats[interface]
                self.log_status(f"\n=== Interface {interface} Statistics ===")
                self.log_status(f"Bytes sent: {stat.bytes_sent:,}")
                self.log_status(f"Bytes received: {stat.bytes_recv:,}")
                self.log_status(f"Packets sent: {stat.packets_sent:,}")
                self.log_status(f"Packets received: {stat.packets_recv:,}")
            else:
                self.log_status(f"Interface {interface} not found in statistics")
                
        except Exception as e:
            self.log_status(f"Error refreshing status: {str(e)}")
    
    def start_monitoring(self):
        """Start network monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self.monitor_network, daemon=True)
            self.monitoring_thread.start()
    
    def monitor_network(self):
        """Monitor network activity"""
        last_stats = None
        
        while self.is_monitoring:
            try:
                interface = self.selected_interface.get()
                if interface:
                    stats = psutil.net_io_counters(pernic=True)
                    if interface in stats:
                        current_stats = stats[interface]
                        
                        if last_stats:
                            bytes_sent_diff = current_stats.bytes_sent - last_stats.bytes_sent
                            bytes_recv_diff = current_stats.bytes_recv - last_stats.bytes_recv
                            
                            # Convert to KB/s
                            upload_speed = bytes_sent_diff / 1024
                            download_speed = bytes_recv_diff / 1024
                            
                            # Update status every 5 seconds
                            if int(time.time()) % 5 == 0:
                                self.root.after(0, self.update_speed_display, 
                                               upload_speed, download_speed)
                        
                        last_stats = current_stats
                
                time.sleep(1)
                
            except Exception:
                time.sleep(1)
    
    def update_speed_display(self, upload_speed, download_speed):
        """Update speed display in status with modern formatting"""
        # Format speeds with units
        def format_speed(speed_kbs):
            if speed_kbs > 1024:
                return f"{speed_kbs/1024:.1f} MB/s"
            else:
                return f"{speed_kbs:.1f} KB/s"
        
        download_formatted = format_speed(download_speed)
        upload_formatted = format_speed(upload_speed)
        
        # Update stat cards
        if hasattr(self, 'download_stat_label') and download_speed > 0:
            self.download_stat_label.config(text=download_formatted)
        if hasattr(self, 'upload_stat_label') and upload_speed > 0:
            self.upload_stat_label.config(text=upload_formatted)
        
        status_msg = f"📊 Real-time → ↓ {download_formatted} | ↑ {upload_formatted}"
        self.log_status(status_msg)
    
    def log_status(self, message):
        """Log message to status text widget with modern formatting"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Color coding for different message types
        if "Error" in message or "Failed" in message:
            prefix = "❌"
            color = "#ff6b6b"
        elif "Success" in message or "set to" in message:
            prefix = "✅"
            color = "#51cf66"
        elif "Warning" in message:
            prefix = "⚠️"
            color = "#ffd43b"
        elif "Current speeds" in message:
            prefix = "📊"
            color = "#74c0fc"
        else:
            prefix = "ℹ️"
            color = "#ffffff"
        
        # Insert message with timestamp
        self.status_text.insert(tk.END, f"[{timestamp}] {prefix} {message}\n")
        self.status_text.see(tk.END)
        
        # Auto-scroll and limit text length
        if int(self.status_text.index('end-1c').split('.')[0]) > 100:
            self.status_text.delete(1.0, 50.0)
    
    def save_settings(self):
        """Save current settings"""
        settings = {
            'interface': self.selected_interface.get(),
            'download_limit': self.current_download_limit.get(),
            'upload_limit': self.current_upload_limit.get()
        }
        
        try:
            with open('speed_limiter_settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass
    
    def load_settings(self):
        """Load saved settings"""
        try:
            if os.path.exists('speed_limiter_settings.json'):
                with open('speed_limiter_settings.json', 'r') as f:
                    settings = json.load(f)
                    
                if 'interface' in settings and settings['interface'] in self.interfaces:
                    self.selected_interface.set(settings['interface'])
                    
        except Exception:
            pass
    
    def on_closing(self):
        """Handle application closing"""
        self.is_monitoring = False
        self.save_settings()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_modern_notification(self, title, message, type="info"):
        """Show modern styled notification"""
        # Create notification window
        notification = tk.Toplevel(self.root)
        notification.title(title)
        notification.geometry("350x150")
        notification.resizable(False, False)
        notification.configure(bg=self.colors['card_bg'])
        
        # Center the notification
        notification.transient(self.root)
        notification.grab_set()
        
        # Position relative to main window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        notification.geometry(f"350x150+{x}+{y}")
        
        # Notification content
        content_frame = tk.Frame(notification, bg=self.colors['card_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon and title
        header_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        if type == "success":
            icon = "✅"
            color = self.colors['success']
        elif type == "error":
            icon = "❌"
            color = self.colors['danger']
        elif type == "warning":
            icon = "⚠️"
            color = self.colors['warning']
        else:
            icon = "ℹ️"
            color = self.colors['accent']
        
        icon_label = tk.Label(header_frame, text=icon, font=('Segoe UI', 16),
                             bg=self.colors['card_bg'], fg=color)
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(header_frame, text=title, font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['card_bg'], fg=self.colors['text'])
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Message
        message_label = tk.Label(content_frame, text=message, font=('Segoe UI', 10),
                                bg=self.colors['card_bg'], fg=self.colors['text_secondary'],
                                wraplength=300, justify=tk.LEFT)
        message_label.pack(pady=(0, 15))
        
        # OK button
        ok_button = tk.Button(content_frame, text="OK", command=notification.destroy,
                             bg=color, fg='white', font=('Segoe UI', 10, 'bold'),
                             border=0, relief='flat', padx=20, pady=8,
                             cursor='hand2')
        ok_button.pack()
        
        # Auto close after 3 seconds for success messages
        if type == "success":
            notification.after(3000, notification.destroy)
        
        # Focus the notification
        notification.focus_set()
    
    def show_error_notification(self, message):
        """Show error notification with modern styling"""
        self.log_status(f"Error: {message}")
        self.show_modern_notification("Error", message, "error")
    
    def show_warning_notification(self, message):
        """Show warning notification with modern styling"""
        self.log_status(f"Warning: {message}")
        self.show_modern_notification("Warning", message, "warning")

    def toggle_maximize(self):
        """Toggle between maximized and normal window state (cross-platform)"""
        try:
            if self.is_windows:
                # Windows toggle
                if self.root.state() == 'zoomed':
                    self.root.state('normal')
                    self.center_window()
                else:
                    self.root.state('zoomed')
            elif self.is_linux:
                # Linux toggle
                if self.root.attributes('-zoomed'):
                    self.root.attributes('-zoomed', False)
                    self.center_window()
                else:
                    self.root.attributes('-zoomed', True)
            else:
                # Fallback for other platforms
                if self.root.winfo_width() > 1000:
                    self.root.geometry("800x600")
                    self.center_window()
                else:
                    self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        except Exception as e:
            # Fallback if toggle fails
            self.root.geometry("1200x800")
            self.center_window()
    
    def center_window(self):
        """Center the window on screen (cross-platform)"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

def main():
    # Cross-platform privilege checking
    current_os = platform.system().lower()
    
    if current_os == 'linux':
        # Check for sudo privileges on Linux
        if os.geteuid() != 0:
            print("Note: This application requires sudo privileges on Linux to modify network settings.")
            print("Run with: sudo python main.py")
            print("Some features may not work without proper permissions.")
    elif current_os == 'windows':
        # Check for admin privileges on Windows
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("Note: Administrator privileges recommended on Windows.")
                print("Some features may require elevated permissions.")
        except:
            print("Note: Could not check administrator status on Windows.")
    
    app = NetworkSpeedController()
    app.run()

if __name__ == "__main__":
    main()
