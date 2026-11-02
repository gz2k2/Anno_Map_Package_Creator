"""Reusable styled application dialog components."""
import customtkinter as ctk

class AppDialog(ctk.CTkToplevel):
    """Provide a modal-looking dialog that follows the application theme."""
    def __init__(self, master, title: str, message: str):
        super().__init__(master)
        self.title(title); self.geometry("520x220"); self.transient(master)
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight="bold")).pack(padx=24, pady=(24,10), anchor="w")
        ctk.CTkLabel(self, text=message, justify="left", wraplength=470).pack(padx=24, pady=10, anchor="w")
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(padx=24, pady=20, anchor="e")
