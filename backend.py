
import json
import os
import ctypes
import sys

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the program with admin rights if not already running as admin."""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def get_network_adapters():
    """Get a list of network adapters."""
    command = "wmic nic where \"NetConnectionStatus=2\" get NetConnectionID"
    try:
        result = os.popen(command).read()
        adapters = [line.strip() for line in result.splitlines() if line.strip() and "NetConnectionID" not in line]
        return adapters
    except Exception as e:
        print(f"Error getting network adapters: {e}")
        return []

def set_dns(adapter_name, dns_servers):
    """Set DNS servers for a specific adapter."""
    try:
        if len(dns_servers) > 0:
            os.system(f"netsh interface ip set dns \"{adapter_name}\" static {dns_servers[0]}")
        if len(dns_servers) > 1:
            os.system(f"netsh interface ip add dns \"{adapter_name}\" {dns_servers[1]} index=2")
        return True
    except Exception as e:
        print(f"Error setting DNS: {e}")
        return False

def clear_dns(adapter_name):
    """Clear DNS settings for a specific adapter."""
    try:
        os.system(f"netsh interface ip set dns \"{adapter_name}\" dhcp")
        return True
    except Exception as e:
        print(f"Error clearing DNS: {e}")
        return False

def load_dns_list():
    """Load the list of saved DNS servers from a JSON file."""
    if not os.path.exists("dns_list.json"):
        return {}
    try:
        with open("dns_list.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_dns_list(dns_list):
    """Save the list of DNS servers to a JSON file."""
    try:
        with open("dns_list.json", "w", encoding='utf-8') as f:
            json.dump(dns_list, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving DNS list: {e}")
