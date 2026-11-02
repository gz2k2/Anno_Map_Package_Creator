"""Styled status window for update-check results."""
import customtkinter as ctk
from app.config.config_app import GITHUB_URL
from app.functions.function_links import open_external_url

class UpdateStatusWindow(ctk.CTkToplevel):
    """Display local/remote version values and update result."""
    def __init__(self, master, result):
        super().__init__(master); self.title("Update Status"); self.geometry("500x300"); self.transient(master)
        messages={"current":"Application is up to date.","update":"A new version is available.","failed":"Update check failed."}
        ctk.CTkLabel(self,text="Update Status",font=ctk.CTkFont(size=22,weight="bold")).pack(pady=(24,14))
        for text in [messages[result.state], f"Current version: {result.local}", f"New version: {result.remote or 'Unavailable'}"]:
            ctk.CTkLabel(self,text=text).pack(pady=5)
        ctk.CTkButton(self,text="Open GitHub Repository",fg_color="#24292f",command=lambda: open_external_url(GITHUB_URL)).pack(pady=18)
        ctk.CTkButton(self,text="Close",command=self.destroy).pack()
