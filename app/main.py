"""Application startup composition for Anno Map Package Creator. It configures the global CustomTkinter appearance and starts the main window."""
import customtkinter as ctk
from app.ui.ui import MainWindow

def run():
    """Perform the run operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    MainWindow().mainloop()
