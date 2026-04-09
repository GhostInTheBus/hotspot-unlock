# TTL Manager Utility (Verizon Bypass Optimized)

A cross-platform desktop application to modify the system's default Time-to-Live (TTL) value. This is specifically optimized for **Verizon** network users to manage hotspot data usage limits by setting the TTL to 65.

*Disclosure: This project was **vibe coded** with the assistance of AI.*

## Features
- **One-Click TTL Modification:** Sets TTL to 65 across Windows, macOS, and Linux.
- **Admin Privilege Management:** Automatically detects and requests administrative/root elevation when needed.
- **Connection Testing:** Built-in "Test Connection" tool that pings localhost and parses the actual active TTL from the response.
- **Safety Reset:** "Reset to Default" button to return system TTL to factory settings (128 for Windows, 64 for Unix-like).

## Architecture & OS Interaction
The application acts as a GUI wrapper for system-level networking commands:
- **Windows:** Interacts with the `netsh` utility to set `defaultcurhoplimit` persistently in the IPv4 stack.
- **macOS/Linux:** Uses the `sysctl` interface to modify kernel parameters (`net.inet.ip.ttl` or `net.ipv4.ip_default_ttl`) in real-time.

## Installation & Requirements
- **Python 3.6+**
- **Tkinter** (usually included with Python; on Linux, you may need `sudo apt-get install python3-tk`).

### Run from Source
```bash
python ttl_utility.py
```

## Compiling to Executable
To create a standalone `.exe` (Windows) or `.app` (macOS), use **PyInstaller**:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Generate the executable:
   ```bash
   # For Windows/Linux (single file, no console)
   pyinstaller --onefile --noconsole ttl_utility.py

   # For macOS (creates a .app bundle)
   pyinstaller --windowed --onefile ttl_utility.py
   ```
   The finished executable will be in the `dist/` folder.

## Security
This application requires administrative privileges to modify system networking parameters. Use with caution.
