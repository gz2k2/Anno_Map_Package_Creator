"""Application composition and startup coordination."""
import customtkinter as ctk
from app.ui.ui import MainWindow

def run() -> None:
    """Configure CustomTkinter and start the UI event loop."""
    ctk.set_appearance_mode("dark"); ctk.set_default_color_theme("blue")
    MainWindow().mainloop()
