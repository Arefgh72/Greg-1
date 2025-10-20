
import json
import os
import ctypes
import sys
from languages import get_text, texts

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
    print(get_text("setting_dns").format(adapter_name=adapter_name))
    if len(dns_servers) > 0:
        os.system(f"netsh interface ip set dns \"{adapter_name}\" static {dns_servers[0]}")
    if len(dns_servers) > 1:
        os.system(f"netsh interface ip add dns \"{adapter_name}\" {dns_servers[1]} index=2")
    print(get_text("dns_set_success"))

def clear_dns(adapter_name):
    """Clear DNS settings for a specific adapter."""
    print(get_text("clearing_dns").format(adapter_name=adapter_name))
    os.system(f"netsh interface ip set dns \"{adapter_name}\" dhcp")
    print(get_text("dns_cleared_success"))

def load_dns_list():
    """Load the list of saved DNS servers from a JSON file."""
    if not os.path.exists("dns_list.json"):
        return {}
    try:
        with open("dns_list.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty dict if file is corrupted or empty

def save_dns_list(dns_list):
    """Save the list of DNS servers to a JSON file."""
    with open("dns_list.json", "w") as f:
        json.dump(dns_list, f, indent=4)

def add_dns_to_list(dns_list):
    """Add a new DNS server to the list."""
    name = input(get_text("enter_dns_name"))
    primary = input(get_text("enter_primary_dns"))
    secondary = input(get_text("enter_secondary_dns"))
    dns_list[name] = [primary, secondary]
    save_dns_list(dns_list)
    print(get_text("dns_added_success"))

def main():
    """Main function to run the DNS manager."""
    global get_text

    while True:
        lang_choice = input("Enter 'en' for English or 'fa' for Persian: ").lower().strip()
        if lang_choice in ['en', 'fa']:
            get_text = lambda key: texts[lang_choice][key]
            break
        else:
            print("Invalid choice. Please enter 'en' or 'fa'.")

    if not is_admin():
        print(get_text("admin_required"))
        input(get_text("press_enter_to_exit"))
        sys.exit()

    dns_list = load_dns_list()

    while True:
        print("\n" + get_text("menu_title"))
        print("1. " + get_text("menu_list_adapters"))
        print("2. " + get_text("menu_add_dns"))
        print("3. " + get_text("menu_set_dns"))
        print("4. " + get_text("menu_clear_dns"))
        print("5. " + get_text("menu_exit"))

        choice = input(get_text("enter_choice")).strip()

        if choice == '1':
            adapters = get_network_adapters()
            print("\n" + get_text("available_adapters"))
            for i, adapter in enumerate(adapters, 1):
                print(f"{i}. {adapter}")

        elif choice == '2':
            add_dns_to_list(dns_list)

        elif choice == '3':
            adapters = get_network_adapters()
            if not adapters:
                print(get_text("no_adapters_found"))
                continue

            print("\n" + get_text("available_adapters"))
            for i, adapter in enumerate(adapters, 1):
                print(f"{i}. {adapter}")

            try:
                adapter_choice_input = input(get_text("select_adapter"))
                adapter_choice = int(adapter_choice_input) - 1
                if not 0 <= adapter_choice < len(adapters):
                    print(get_text("invalid_choice"))
                    continue
            except ValueError:
                print(get_text("invalid_input"))
                continue

            if not dns_list:
                print(get_text("no_dns_profiles"))
                continue

            print("\n" + get_text("select_dns_from_list"))
            saved_dns_names = list(dns_list.keys())
            for i, name in enumerate(saved_dns_names, 1):
                print(f"{i}. {name} ({dns_list[name][0]}, {dns_list[name][1]})")

            try:
                dns_choice_input = input(get_text("select_dns"))
                dns_choice = int(dns_choice_input) - 1
                if not 0 <= dns_choice < len(saved_dns_names):
                    print(get_text("invalid_choice"))
                    continue
            except ValueError:
                print(get_text("invalid_input"))
                continue

            selected_adapter = adapters[adapter_choice]
            selected_dns_name = saved_dns_names[dns_choice]
            selected_dns_servers = dns_list[selected_dns_name]

            set_dns(selected_adapter, selected_dns_servers)

        elif choice == '4':
            adapters = get_network_adapters()
            if not adapters:
                print(get_text("no_adapters_found"))
                continue

            print("\n" + get_text("available_adapters"))
            for i, adapter in enumerate(adapters, 1):
                print(f"{i}. {adapter}")

            try:
                adapter_choice_input = input(get_text("select_adapter_to_clear"))
                adapter_choice = int(adapter_choice_input) - 1
                if not 0 <= adapter_choice < len(adapters):
                    print(get_text("invalid_choice"))
                    continue
            except ValueError:
                print(get_text("invalid_input"))
                continue

            selected_adapter = adapters[adapter_choice]
            clear_dns(selected_adapter)

        elif choice == '5':
            break

        else:
            print(get_text("invalid_choice"))

if __name__ == "__main__":
    main()
