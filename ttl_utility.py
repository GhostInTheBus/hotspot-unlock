import os
import sys
import platform
import subprocess
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext

class TTLUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verizon TTL Utility")
        self.root.geometry("500x450")
        
        self.os_type = platform.system()
        self.is_admin = self.check_admin()
        
        self.setup_ui()
        self.log("Verizon Optimized TTL Manager (TTL=65)")
        self.log("Vibe coded by Gemini CLI.")
        self.log(f"Detected OS: {self.os_type}")
        self.log(f"Admin Privileges: {'Yes' if self.is_admin else 'No'}")
        
        if not self.is_admin:
            self.log("WARNING: Certain features require administrative privileges.")

    def check_admin(self):
        """Check if the current process has administrative/root privileges."""
        try:
            if self.os_type == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except AttributeError:
            return False

    def elevate(self):
        """Re-run the script with administrative privileges."""
        if self.os_type == "Windows":
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        elif self.os_type in ["Darwin", "Linux"]:
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        sys.exit()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="Verizon TTL Manager", font=("Arial", 16, "bold")).pack(pady=(10, 0))
        tk.Label(self.root, text="Changes TTL so usage registers as phone data, not hotspot.", font=("Arial", 9, "italic"), fg="#555").pack(pady=(0, 10))
        
        # Action Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Set TTL to 65", command=self.set_ttl_65, width=20, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Reset to Default", command=self.reset_ttl, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Test Connection (Ping)", command=self.test_connection, width=20, bg="#2196F3", fg="white").grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Elevate to Admin", command=self.elevate, width=20).grid(row=1, column=1, padx=5, pady=5)

        # Log Output
        tk.Label(self.root, text="Activity Log:").pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(self.root, height=12, width=55)
        self.log_area.pack(padx=20, pady=5)

    def log(self, message):
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)

    def run_command(self, cmd):
        """Utility to run shell commands and return output."""
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.log(f"Error: {e.stderr.strip()}")
            return None

    def set_ttl_65(self):
        if not self.is_admin:
            if messagebox.askyesno("Admin Required", "This action requires administrative privileges. Elevate now?"):
                self.elevate()
            return

        self.log("Setting TTL to 65...")
        if self.os_type == "Windows":
            cmd = "netsh int ipv4 set global defaultcurhoplimit=65 store=persistent"
        elif self.os_type == "Darwin":
            cmd = "sysctl -w net.inet.ip.ttl=65"
        elif self.os_type == "Linux":
            cmd = "sysctl -w net.ipv4.ip_default_ttl=65"
        else:
            self.log("Unsupported OS for this operation.")
            return

        if self.run_command(cmd) is not None:
            self.log("Successfully set TTL to 65.")

    def reset_ttl(self):
        if not self.is_admin:
            messagebox.showwarning("Admin Required", "Please elevate to administrator to reset TTL.")
            return

        default_ttl = 128 if self.os_type == "Windows" else 64
        self.log(f"Resetting TTL to default ({default_ttl})...")
        
        if self.os_type == "Windows":
            cmd = f"netsh int ipv4 set global defaultcurhoplimit={default_ttl} store=persistent"
        elif self.os_type == "Darwin":
            cmd = f"sysctl -w net.inet.ip.ttl={default_ttl}"
        elif self.os_type == "Linux":
            cmd = f"sysctl -w net.ipv4.ip_default_ttl={default_ttl}"
        
        if self.run_command(cmd) is not None:
            self.log(f"Successfully reset TTL to {default_ttl}.")

    def test_connection(self):
        self.log("Testing connection (pinging localhost)...")
        ping_cmd = "ping -n 1 127.0.0.1" if self.os_type == "Windows" else "ping -c 1 127.0.0.1"
        output = self.run_command(ping_cmd)
        
        if output:
            # Parse TTL from output using Regex (case insensitive)
            ttl_match = re.search(r"ttl=(\d+)", output, re.IGNORECASE)
            if ttl_match:
                current_ttl = ttl_match.group(1)
                self.log(f"Test Successful! Current Active TTL: {current_ttl}")
                if current_ttl == "65":
                    self.log("CONFIRMED: Your connection is using the custom TTL (65).")
                else:
                    self.log(f"NOTICE: System is currently using TTL {current_ttl}.")
            else:
                self.log("Could not parse TTL from ping output.")
                self.log(f"Raw Output: {output}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TTLUtilityApp(root)
    root.mainloop()
