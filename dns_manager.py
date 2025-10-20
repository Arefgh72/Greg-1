
import json
import os
import ctypes
import sys
from languages import get_text, texts
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Set console to UTF-8
os.system("chcp 65001")
os.system("cls") # Clear the console screen

# Global variable to hold the selected language
selected_language = 'en'

def display_text(text):
    """Reshape and apply bidi algorithm for Persian text."""
    if selected_language == 'fa':
        return get_display(reshape(text))
    return text

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_network_adapters():
    """Get a list of network adapters."""
    command = "wmic nic where \"NetConnectionStatus=2\" get NetConnectionID"
    result = os.popen(command).read()
    adapters = [line.strip() for line in result.splitlines() if line.strip() and "NetConnectionID" not in line]
    return adapters

def set_dns(adapter_name, dns_servers):
    """Set DNS servers for a specific adapter."""
    print(display_text(get_text("setting_dns").format(adapter_name=adapter_name)))
    if len(dns_servers) > 0:
        os.system(f"netsh interface ip set dns \"{adapter_name}\" static {dns_servers[0]}")
    if len(dns_servers) > 1:
        os.system(f"netsh interface ip add dns \"{adapter_name}\" {dns_servers[1]} index=2")
    print(display_text(get_text("dns_set_success")))

def clear_dns(adapter_name):
    """Clear DNS settings for a specific adapter."""
    print(display_text(get_text("clearing_dns").format(adapter_name=adapter_name)))
    os.system(f"netsh interface ip set dns \"{adapter_name}\" dhcp")
    print(display_text(get_text("dns_cleared_success")))

def load_dns_list():
    """Load the list of saved DNS servers from a JSON file."""
    if not os.path.exists("dns_list.json"):
        return {}
    try:
        with open("dns_list.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_dns_list(dns_list):
    """Save the list of DNS servers to a JSON file."""
    with open("dns_list.json", "w", encoding='utf-8') as f:
        json.dump(dns_list, f, indent=4, ensure_ascii=False)

def add_dns_to_list(dns_list):
    """Add a new DNS server to the list."""
    name = input(display_text(get_text("enter_dns_name")))
    primary = input(display_text(get_text("enter_primary_dns")))
    secondary = input(display_text(get_text("enter_secondary_dns")))
    dns_list[name] = [primary, secondary]
    save_dns_list(dns_list)
    print(display_text(get_text("dns_added_success")))

def main():
    """Main function to run the DNS manager."""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    global get_text, selected_language

    while True:
        lang_prompt = "Enter 'en' for English or 'fa' for Persian: "
        # We need to display the Persian part of the prompt correctly
        fa_prompt = get_display(reshape("برای زبان فارسی 'fa' را وارد کنید: "))
        lang_choice = input(f"{lang_prompt}\n{fa_prompt}").lower().strip()

        if lang_choice in ['en', 'fa']:
            selected_language = lang_choice
            get_text = lambda key: texts[selected_language][key]
            break
        else:
            print("Invalid choice. Please enter 'en' or 'fa'.")

    dns_list = load_dns_list()

    while True:
        print("\n" + display_text(get_text("menu_title")))
        print("1. " + display_text(get_text("menu_list_adapters")))
        print("2. " + display_text(get_text("menu_add_dns")))
        print("3. " + display_text(get_text("menu_set_dns")))
        print("4. " + display_text(get_text("menu_clear_dns")))
        print("5. " + display_text(get_text("menu_exit")))

        choice = input(display_text(get_text("enter_choice"))).strip()

        if choice == '1':
            adapters = get_network_adapters()
            print("\n" + display_text(get_text("available_adapters")))
            for i, adapter in enumerate(adapters, 1):
                print(f"{i}. {adapter}")

        elif choice == '2':
            add_dns_to_list(dns_list)

        elif choice == '3':
            adapters = get_network_adapters()
            if not adapters:
                print(display_text(get_text("no_adapters_found")))
                continue

            print("\n" + display_text(get_text("available_adapters")))
            for i, adapter in enumerate(adapters, 1):
                print(f"{i}. {adapter}")

            try:
                adapter_choice_input = input(display_text(get_text("select_adapter")))
                adapter_choice = int(adapter_choice_input) - 1
                if not 0 <= adapter_choice < len(adapters):
                    print(display_text(get_text("invalid_choice")))
                    continue
            except ValueError:
                print(display_text(get_text("invalid_input")))
                continue

            if not dns_list:
                print(display_text(get_text("no_dns_profiles")))
                continue

            print("\n" + display_text(get_text("select_dns_from_list")))
            saved_dns_names = list(dns_list.keys())
            for i, name in enumerate(saved_dns_names, 1):
                # Displaying DNS profile names correctly if they are in Persian
                display_name = display_text(name)
                print(f"{i}. {display_name} ({dns_list[name][0]}, {dns_list[name][1]})")

            try:
                dns_choice_input = input(display_text(get_text("select_dns")))
                dns_choice = int(dns_choice_input) - 1
                if not 0 <= dns_choice < len(saved_dns_names):
                    print(display_text(get_text("invalid_choice")))
                    continue
            except ValueError:
                print(display_text(get_text("invalid_input")))
                continue

            selected_adapter = adapters[adapter_choice]
            selected_dns_name = saved_dns_names[dns_choice]
            selected_dns_servers = dns_list[selected_dns_name]

            set_dns(selected_adapter, selected_dns_servers)

        elif choice == '4':
            adapters = get_network_adapters()
            if not adapters:
                print(display_text(get_text("no_adapters_found")))
                continue

            print("\n" + display_text(get_text("available_adapters")))
            for i, adapter in enumerate(adapters, 1):
                print(f"{i}. {adapter}")

            try:
                adapter_choice_input = input(display_text(get_text("select_adapter_to_clear")))
                adapter_choice = int(adapter_choice_input) - 1
                if not 0 <= adapter_choice < len(adapters):
                    print(display_text(get_text("invalid_choice")))
                    continue
            except ValueError:
                print(display_text(get_text("invalid_input")))
                continue

            selected_adapter = adapters[adapter_choice]
            clear_dns(selected_adapter)

        elif choice == '5':
            break

        else:
            print(display_text(get_text("invalid_choice")))

if __name__ == "__main__":
    main()
