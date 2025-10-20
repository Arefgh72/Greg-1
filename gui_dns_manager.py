
import customtkinter as ctk
from tkinter import messagebox
import backend
from languages import texts

class AddDnsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.name_entry = ctk.CTkEntry(self, width=250)
        self.name_entry.pack(padx=20, pady=(20, 5))
        self.primary_entry = ctk.CTkEntry(self, width=250)
        self.primary_entry.pack(padx=20, pady=5)
        self.secondary_entry = ctk.CTkEntry(self, width=250)
        self.secondary_entry.pack(padx=20, pady=5)
        self.save_button = ctk.CTkButton(self, command=self.save_dns)
        self.save_button.pack(padx=20, pady=(10, 20))

        self.update_ui_text()

    def save_dns(self):
        name = self.name_entry.get().strip()
        primary = self.primary_entry.get().strip()
        secondary = self.secondary_entry.get().strip()
        if name and primary:
            self.master.add_dns_profile(name, primary, secondary)
            self.destroy()

    def update_ui_text(self):
        lang = self.master.current_language
        self.title(texts[lang]["add_dns_title"])
        self.name_entry.configure(placeholder_text=texts[lang]["add_dns_name"])
        self.primary_entry.configure(placeholder_text=texts[lang]["add_dns_primary"])
        self.secondary_entry.configure(placeholder_text=texts[lang]["add_dns_secondary"])
        self.save_button.configure(text=texts[lang]["add_dns_save"])

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        backend.run_as_admin()

        self.geometry("750x450")
        self.minsize(600, 350)
        ctk.set_appearance_mode("System")
        self.current_language = "en"
        self.selected_adapter = ctk.StringVar()
        self.selected_dns = ctk.StringVar()

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Labels
        self.adapters_label = ctk.CTkLabel(self, font=("Arial", 16))
        self.adapters_label.grid(row=0, column=0, pady=(10, 5))
        self.dns_label = ctk.CTkLabel(self, font=("Arial", 16))
        self.dns_label.grid(row=0, column=1, pady=(10, 5))

        # Lists
        self.adapters_list = ctk.CTkScrollableFrame(self)
        self.adapters_list.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.dns_list_frame = ctk.CTkScrollableFrame(self)
        self.dns_list_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        # Buttons
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.apply_button = ctk.CTkButton(self.buttons_frame, command=self.apply_dns)
        self.apply_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.clear_button = ctk.CTkButton(self.buttons_frame, command=self.clear_dns)
        self.clear_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.add_button = ctk.CTkButton(self.buttons_frame, command=self.open_add_dns_window)
        self.add_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.delete_button = ctk.CTkButton(self.buttons_frame, command=self.delete_dns)
        self.delete_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.lang_button = ctk.CTkButton(self.buttons_frame, command=self.toggle_language)
        self.lang_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        self.update_ui_text()
        self.populate_lists()

    def populate_lists(self):
        # Clear existing widgets
        for widget in self.adapters_list.winfo_children(): widget.destroy()
        for widget in self.dns_list_frame.winfo_children(): widget.destroy()

        # Populate Adapters
        adapters = backend.get_network_adapters()
        for adapter in adapters:
            rb = ctk.CTkRadioButton(self.adapters_list, text=adapter, variable=self.selected_adapter, value=adapter)
            rb.pack(fill="x", padx=10, pady=2)

        # Populate DNS Profiles
        self.dns_profiles = backend.load_dns_list()
        for name in self.dns_profiles.keys():
            rb = ctk.CTkRadioButton(self.dns_list_frame, text=name, variable=self.selected_dns, value=name)
            rb.pack(fill="x", padx=10, pady=2)

    def apply_dns(self):
        adapter = self.selected_adapter.get()
        dns_name = self.selected_dns.get()
        if not adapter:
            messagebox.showerror(texts[self.current_language]["error_title"], texts[self.current_language]["adapter_not_selected"])
            return
        if not dns_name:
            messagebox.showerror(texts[self.current_language]["error_title"], texts[self.current_language]["dns_not_selected"])
            return

        dns_servers = self.dns_profiles[dns_name]
        if backend.set_dns(adapter, dns_servers):
            messagebox.showinfo(texts[self.current_language]["success_title"], texts[self.current_language]["dns_set_success"])

    def clear_dns(self):
        adapter = self.selected_adapter.get()
        if not adapter:
            messagebox.showerror(texts[self.current_language]["error_title"], texts[self.current_language]["adapter_not_selected"])
            return
        if backend.clear_dns(adapter):
            messagebox.showinfo(texts[self.current_language]["success_title"], texts[self.current_language]["dns_cleared_success"])

    def open_add_dns_window(self):
        AddDnsWindow(self)

    def add_dns_profile(self, name, primary, secondary):
        self.dns_profiles[name] = [primary, secondary] if secondary else [primary]
        backend.save_dns_list(self.dns_profiles)
        self.populate_lists()

    def delete_dns(self):
        dns_name = self.selected_dns.get()
        if not dns_name:
            messagebox.showerror(texts[self.current_language]["error_title"], texts[self.current_language]["dns_not_selected"])
            return

        confirm = messagebox.askyesno(
            texts[self.current_language]["delete_dns_title"],
            texts[self.current_language]["delete_dns_confirm"]
        )
        if confirm:
            del self.dns_profiles[dns_name]
            backend.save_dns_list(self.dns_profiles)
            self.selected_dns.set("")
            self.populate_lists()

    def toggle_language(self):
        self.current_language = "fa" if self.current_language == "en" else "en"
        self.update_ui_text()

    def update_ui_text(self):
        lang = self.current_language
        self.title(texts[lang]["app_title"])
        self.adapters_label.configure(text=texts[lang]["adapters_label"])
        self.dns_label.configure(text=texts[lang]["dns_label"])
        self.apply_button.configure(text=texts[lang]["apply_button"])
        self.clear_button.configure(text=texts[lang]["clear_button"])
        self.add_button.configure(text=texts[lang]["add_button"])
        self.delete_button.configure(text=texts[lang]["delete_button"])
        self.lang_button.configure(text=texts[lang]["lang_button"])

if __name__ == "__main__":
    app = App()
    app.mainloop()
