"""CustomTkinter presentation and worker coordination for map-package export."""
from pathlib import Path
from queue import Empty, Queue
import threading
import customtkinter as ctk
from tkinter import filedialog
from app.functions.function_database import get_package, package_entries, package_names
from app.functions.function_settings import load_settings
from app.models.model_export import ExportRequest
from app.services.service_map_export import export_map_package
from app.templates.template_dialog import AppDialog, ConfirmDialog

class ExportMapsAsModTab(ctk.CTkFrame):
    """Collect export input, run the export worker, and display its live log."""

    def __init__(self, master, selected_game: str):
        """Build the export tab for the initially selected game."""
        super().__init__(master)
        self.game = ctk.StringVar(value=selected_game)
        self.map_package = ctk.StringVar()
        self.export_folder = ctk.StringVar()
        self.status = ctk.StringVar(value='Ready')
        self._messages: Queue = Queue()
        self._worker: threading.Thread | None = None
        self._build_widgets()
        self._apply_default_export_path()
        self.reload()
        self.after(75, self._poll_worker_messages)

    def _build_widgets(self) -> None:
        """Create the input controls, action row, and read-only autoscrolling log."""
        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=18, pady=18)
        content.grid_columnconfigure(1, weight=0)
        content.grid_columnconfigure(3, weight=1)
        content.grid_rowconfigure(3, weight=1)
        ctk.CTkLabel(content, text='Island Package').grid(row=0, column=0, padx=(0, 12), pady=8, sticky='w')
        self.package_menu = ctk.CTkOptionMenu(content, values=[''], variable=self.map_package, width=220)
        self.package_menu.grid(row=0, column=1, columnspan=2, pady=8, sticky='w')
        ctk.CTkLabel(content, text='Export Folder').grid(row=1, column=0, padx=(0, 12), pady=8, sticky='w')
        ctk.CTkEntry(content, textvariable=self.export_folder, state='readonly', width=420).grid(row=1, column=1, padx=(0, 8), pady=8, sticky='w')
        ctk.CTkButton(content, text='Browse...', width=100, command=self.select_folder).grid(row=1, column=2, pady=8)
        action = ctk.CTkFrame(content, fg_color='transparent')
        action.grid(row=2, column=0, columnspan=4, pady=(12, 8), sticky='ew')
        ctk.CTkLabel(action, textvariable=self.status).pack(side='left')
        self.export_button = ctk.CTkButton(action, text='Export Island Package as Mod', command=self.export)
        self.export_button.pack(side='right')
        frame = ctk.CTkFrame(content)
        frame.grid(row=3, column=0, columnspan=4, sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(frame, text='Export Log', font=ctk.CTkFont(weight='bold')).grid(row=0, column=0, padx=12, pady=8, sticky='w')
        self.log = ctk.CTkTextbox(frame, state='disabled', wrap='none')
        self.log.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')

    def reload(self) -> None:
        """Reload alphabetically sorted packages for the selected game."""
        values = sorted(package_names(self.game.get()), key=str.casefold)
        current = self.map_package.get()
        self.package_menu.configure(values=values or [''])
        self.map_package.set(current if current in values else values[0] if values else '')

    def set_game(self, game: str) -> None:
        """Switch the export context and load its default export path and packages."""
        self.game.set(game)
        self._apply_default_export_path()
        self.reload()

    def _apply_default_export_path(self) -> None:
        """Load the game-specific default export path from persisted settings."""
        settings = load_settings()
        value = settings.get('games', {}).get(self.game.get(), {}).get('default_export_path', '')
        self.export_folder.set(value)

    def select_folder(self) -> None:
        """Let the user select a temporary export folder for the current operation."""
        value = filedialog.askdirectory(parent=self, title='Select Export Folder', initialdir=self.export_folder.get() or None)
        if value:
            self.export_folder.set(value)

    def export(self) -> None:
        """Validate UI input and request confirmation before replacing an existing mod."""
        if self._worker and self._worker.is_alive():
            return
        try:
            request = self._build_request()
        except (ValueError, OSError) as error:
            AppDialog(self, 'Export Failed', str(error))
            return
        if request.target.exists():
            ConfirmDialog(self, 'Replace Existing Mod', f'The folder "{request.target.name}" already exists. Replace it?', lambda: self._start_worker(request))
        else:
            self._start_worker(request)

    def _build_request(self) -> ExportRequest:
        """Build and validate the immutable service request from current UI state."""
        package_name = self.map_package.get().strip()
        if not package_name:
            raise ValueError('Select a Map Package first.')
        package = get_package(self.game.get(), package_name)
        if not package:
            raise ValueError('The selected Map Package no longer exists.')
        mod_name = str(package.get('mod_name', '')).strip()
        if not mod_name:
            raise ValueError('Set Mod Name in the Island Packages tab first.')
        if any((character in mod_name for character in '<>:"/\\|?*')):
            raise ValueError('Mod Name contains invalid Windows filename characters.')
        export_root = Path(self.export_folder.get().strip())
        if not export_root.is_dir():
            raise ValueError('Select an existing Export Folder first.')
        entries = tuple(package_entries(self.game.get(), package_name))
        if not entries:
            raise ValueError('The selected Map Package does not contain any maps.')
        package_id = str(package.get('id', '')).strip()
        if not package_id:
            raise ValueError('The selected Map Package has no internal ID.')
        return ExportRequest(game=self.game.get(), target=export_root / f'[IslandPackage] {mod_name}', package_id=package_id, package=dict(package), entries=entries, settings=load_settings())

    def _start_worker(self, request: ExportRequest) -> None:
        """Start the blocking export service on a daemon worker thread."""
        self._clear_log()
        self.export_button.configure(state='disabled')
        self.status.set('Exporting...')
        self._write_log(f'Target: {request.target}')
        self._worker = threading.Thread(target=self._worker_entry, args=(request,), daemon=True)
        self._worker.start()

    def _worker_entry(self, request: ExportRequest) -> None:
        """Execute the service and forward logs, completion, or errors to the UI queue."""
        try:
            result = export_map_package(request, lambda text: self._messages.put(('log', text)))
            self._messages.put(('done', result))
        except (OSError, ValueError) as error:
            self._messages.put(('error', str(error)))

    def _poll_worker_messages(self) -> None:
        """Apply worker messages on the Tk UI thread and maintain autoscroll."""
        try:
            while True:
                kind, payload = self._messages.get_nowait()
                if kind == 'log':
                    self._write_log(payload)
                elif kind == 'done':
                    self.status.set('Export complete')
                    self.export_button.configure(state='normal')
                    AppDialog(self, 'Export Complete', f'Exported {payload.copied_folders} map folder(s) and {payload.copied_files} file(s) to:\n{payload.target}')
                elif kind == 'error':
                    self._write_log(f'ERROR: {payload}')
                    self.status.set('Export failed')
                    self.export_button.configure(state='normal')
                    AppDialog(self, 'Export Failed', payload)
        except Empty:
            pass
        self.after(75, self._poll_worker_messages)

    def _write_log(self, text: str) -> None:
        """Append one read-only log line and keep the newest line visible."""
        self.log.configure(state='normal')
        self.log.insert('end', text + '\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def _clear_log(self) -> None:
        """Clear the log before a new export begins."""
        self.log.configure(state='normal')
        self.log.delete('1.0', 'end')
        self.log.configure(state='disabled')
