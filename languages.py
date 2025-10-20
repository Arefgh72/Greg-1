
texts = {
    'en': {
        "admin_required": "Administrator privileges are required to run this script.",
        "press_enter_to_exit": "Press Enter to exit.",
        "menu_title": "DNS Manager Menu",
        "menu_list_adapters": "List Network Adapters",
        "menu_add_dns": "Add New DNS",
        "menu_set_dns": "Set DNS",
        "menu_clear_dns": "Clear DNS",
        "menu_exit": "Exit",
        "enter_choice": "Enter your choice: ",
        "available_adapters": "Available network adapters:",
        "select_adapter": "Select an adapter (number): ",
        "select_dns_from_list": "Select a DNS from the list:",
        "select_dns": "Select a DNS (number): ",
        "dns_set_success": "DNS set successfully.",
        "select_adapter_to_clear": "Select an adapter to clear DNS (number): ",
        "dns_cleared_success": "DNS cleared successfully.",
        "enter_dns_name": "Enter a name for the DNS: ",
        "enter_primary_dns": "Enter the primary DNS: ",
        "enter_secondary_dns": "Enter the secondary DNS: ",
        "dns_added_success": "DNS added successfully.",
        "invalid_input": "Invalid input. Please enter a valid number.",
        "invalid_choice": "Invalid choice. Please try again.",
        "no_adapters_found": "No active network adapters found.",
        "no_dns_profiles": "No DNS profiles saved. Please add one first.",
        "setting_dns": "Setting DNS for {adapter_name}...",
        "clearing_dns": "Clearing DNS for {adapter_name}..."
    },
    'fa': {
        "admin_required": "برای اجرای این برنامه نیاز به دسترسی ادمین دارید.",
        "press_enter_to_exit": "برای خروج، کلید Enter را فشار دهید.",
        "menu_title": "منوی مدیریت DNS",
        "menu_list_adapters": "نمایش کارت‌های شبکه",
        "menu_add_dns": "افزودن DNS جدید",
        "menu_set_dns": "تنظیم DNS",
        "menu_clear_dns": "پاک کردن DNS",
        "menu_exit": "خروج",
        "enter_choice": "گزینه خود را وارد کنید: ",
        "available_adapters": "کارت‌های شبکه موجود:",
        "select_adapter": "یک کارت شبکه را انتخاب کنید (شماره): ",
        "select_dns_from_list": "یک DNS از لیست انتخاب کنید:",
        "select_dns": "یک DNS را انتخاب کنید (شماره): ",
        "dns_set_success": "DNS با موفقیت تنظیم شد.",
        "select_adapter_to_clear": "یک کارت شبکه را برای پاک کردن DNS انتخاب کنید (شماره): ",
        "dns_cleared_success": "DNS با موفقیت پاک شد.",
        "enter_dns_name": "یک نام برای DNS وارد کنید: ",
        "enter_primary_dns": "DNS اصلی را وارد کنید: ",
        "enter_secondary_dns": "DNS جایگزین را وارد کنید: ",
        "dns_added_success": "DNS با موفقیت اضافه شد.",
        "invalid_input": "ورودی نامعتبر است. لطفاً یک شماره معتبر وارد کنید.",
        "invalid_choice": "گزینه نامعتبر است. لطفاً دوباره تلاش کنید.",
        "no_adapters_found": "هیچ کارت شبکه فعالی یافت نشد.",
        "no_dns_profiles": "هیچ پروفایل DNS ذخیره نشده است. لطفاً ابتدا یکی اضافه کنید.",
        "setting_dns": "در حال تنظیم DNS برای {adapter_name}...",
        "clearing_dns": "در حال پاک کردن DNS برای {adapter_name}..."
    }
}

def get_text(key):
    # This function will be replaced by the one in main() after language selection
    return texts['en'][key]
