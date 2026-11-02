"""Export Maps as Mod tab."""
import customtkinter as ctk


class ExportMapsAsModTab(ctk.CTkFrame):
    """Host the future map-mod export workflow."""

    def __init__(self, master):
        super().__init__(master)
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            content,
            text="Export Maps as Mod",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w")
