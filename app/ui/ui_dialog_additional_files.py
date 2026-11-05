"""Additional Files dialog for a Map Package. It manages the dialog presentation and user selection state while delegating persistence to the database function layer."""
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from app.functions.function_database import get_package, update_package_additional_files
from app.templates.template_dialog import AppDialog
from app.templates.template_table import SortableTable

class AdditionalFilesDialog(ctk.CTkToplevel):
    """Represent the AdditionalFilesDialog component and own its lifecycle within this module."""

    def __init__(self, master, game, package_name, on_saved=None):
        """Perform the init operation for this module responsibility.

Args:
    master: Input used by the init operation.
    game: Input used by the init operation.
    package_name: Input used by the init operation.
    on_saved: Input used by the init operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        super().__init__(master, fg_color='#1f1f1f')
        self.game = game
        self.package_name = package_name
        self.on_saved = on_saved
        self.title('Additional Files')
        self.geometry('820x480')
        self.minsize(650, 380)
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.after(10, self._apply_windows_dark_titlebar)
        self.grab_set()
        package = get_package(game, package_name) or {}
        self.mod_name = str(package.get('mod_name', '')).strip() or package_name
        self.folders = list(package.get('additional_files', []))
        self._build()
        self._reload()

    def _apply_windows_dark_titlebar(self):
        """Perform the apply windows dark titlebar operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        try:
            import ctypes
            if not hasattr(ctypes, 'windll'):
                return
            self.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            enabled = ctypes.c_int(1)
            for attribute in (20, 19):
                if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attribute, ctypes.byref(enabled), ctypes.sizeof(enabled)) == 0:
                    break
        except (AttributeError, OSError):
            pass

    def _build(self):
        """Perform the build operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        top = ctk.CTkFrame(self, fg_color='#1f1f1f')
        top.pack(fill='x', padx=16, pady=(16, 8))
        ctk.CTkButton(top, text='Add Files', command=self.add_folder).pack(side='left')
        self.table = SortableTable(self, [('Root', 'Root Folder', 160), ('Folder', 'Source Folder', 430), ('Export', 'Export Example', 360)])
        self.table.pack(fill='both', expand=True, padx=16, pady=8)
        self.tree = self.table.tree
        self.menu = tk.Menu(self, tearoff=0, bg='#2b2b2b', fg='#f2f2f2', activebackground='#1f6aa5', activeforeground='#ffffff', bd=0)
        self.menu.add_command(label='Delete', command=self.delete_selected)
        self.tree.bind('<Button-3>', self._popup)
        bottom = ctk.CTkFrame(self, fg_color='#1f1f1f')
        bottom.pack(fill='x', padx=16, pady=(8, 16))
        ctk.CTkButton(bottom, text='Save', command=self.save).pack(side='right')

    def _reload(self):
        """Perform the reload operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        rows = []
        for folder in self.folders:
            source = Path(folder)
            try:
                first = next(iter(sorted(source.iterdir(), key=lambda item: item.name.casefold())), None) if source.is_dir() else None
            except OSError:
                first = None
            example = first.name if first else '...'
            rows.append((source.name, folder, f'[MapPackage] {self.mod_name}\\{example}'))
        self.table.set_rows(rows)

    def add_folder(self):
        """Perform the add folder operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        folder = filedialog.askdirectory(parent=self, title='Select Additional Files Root Folder')
        if folder and folder.casefold() not in {x.casefold() for x in self.folders}:
            self.folders.append(folder)
            self._reload()

    def _popup(self, event):
        """Perform the popup operation for this module responsibility.

Args:
    event: Input used by the popup operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        row = self.tree.identify_row(event.y)
        if not row:
            return
        if row not in self.tree.selection():
            self.tree.selection_set(row)
        self.menu.tk_popup(event.x_root, event.y_root)

    def delete_selected(self):
        """Perform the delete selected operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        selected = set(self.tree.selection())
        self.folders = [folder for item, folder in zip(self.tree.get_children(), self.folders) if item not in selected]
        self._reload()

    def save(self):
        """Perform the save operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        try:
            update_package_additional_files(self.game, self.package_name, self.folders)
        except (ValueError, OSError) as error:
            AppDialog(self, 'Additional Files', str(error))
            return
        if self.on_saved:
            self.on_saved()
        self.destroy()
