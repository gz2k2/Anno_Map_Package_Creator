"""Main application window, persistent header controls, and primary tab coordination."""
import customtkinter as ctk
import threading

from app.config.config_app import GITHUB_URL, KOFI_URL
from app.config.config_paths import version_path
from app.functions.function_links import open_external_url
from app.functions.function_update_check import check_for_update
from app.functions.function_settings import load_settings, save_settings
from app.templates.template_dialog import AppDialog
from app.ui.tabs.ui_tab_export_maps import ExportMapsAsModTab
from app.ui.tabs.ui_tab_general import GeneralTab
from app.ui.tabs.ui_tab_packages import MapPackagesTab
from app.ui.tabs.ui_tab_settings import SettingsTab
from app.ui.ui_update_status import UpdateStatusWindow

# Change this constant to rename the application without touching window logic.
APP_TITLE = "Anno Map Package Creator by gz2k2"


class MainWindow(ctk.CTk):
    """Own the persistent header, game selector, tabs, and application-wide refresh wiring."""

    def __init__(self):
        """Initialize the window from persisted settings and the authoritative version file."""
        super().__init__()
        version = self._read_version()
        self.title(f"{APP_TITLE} v{version}")
        self.geometry("1120x700")
        self.settings = load_settings()
        self._build_header()
        self._build_tabs()
        self.after(500, self._start_update_check)

    def _start_update_check(self) -> None:
        """Start the update check without blocking the CustomTkinter UI thread."""
        threading.Thread(target=self._update_check_worker, daemon=True).start()

    def _update_check_worker(self) -> None:
        """Run the network check in the background and show its result on the UI thread."""
        result = check_for_update()
        self.after(0, lambda: UpdateStatusWindow(self, result))

    def _read_version(self) -> str:
        """Read version.txt for the window title and return a safe fallback when unavailable."""
        try:
            value = version_path().read_text(encoding="utf-8").strip()
            return value or "unknown"
        except OSError:
            return "unknown"

    def _build_header(self) -> None:
        """Build the always-visible game toggle and external-link buttons."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(14, 0))
        ctk.CTkLabel(header, text="Game", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(4, 10))
        self.game_toggle = ctk.CTkSegmentedButton(
            header,
            values=["Anno 117", "Anno 1800"],
            command=self.game_changed,
        )
        self.game_toggle.pack(side="left")
        self.game_toggle.set(self.settings["selected_game"])
        ctk.CTkButton(
            header,
            text="Ko-fi",
            width=82,
            fg_color="#8b4a3b",
            hover_color="#a65c4b",
            command=lambda: open_external_url(KOFI_URL),
        ).pack(side="right", padx=(8, 4))
        ctk.CTkButton(
            header,
            text="GitHub",
            width=82,
            fg_color="#24292f",
            hover_color="#3a3f45",
            command=lambda: open_external_url(GITHUB_URL),
        ).pack(side="right", padx=4)

    def _build_tabs(self) -> None:
        """Create the primary tabs and connect cross-tab refresh callbacks."""
        tabs = ctk.CTkTabview(self)
        tabs.pack(fill="both", expand=True, padx=14, pady=(6, 14))
        for name in ("General", "Map Packages", "Export Maps as Mod", "Settings"):
            tabs.add(name)
        self.general = GeneralTab(tabs.tab("General"), self.settings["selected_game"], self.game_changed, self.current_settings)
        self.general.pack(fill="both", expand=True)
        self.packages_tab = MapPackagesTab(tabs.tab("Map Packages"), self.settings["selected_game"])
        self.packages_tab.pack(fill="both", expand=True)
        self.export_maps_tab = ExportMapsAsModTab(tabs.tab("Export Maps as Mod"), self.settings["selected_game"])
        self.export_maps_tab.pack(fill="both", expand=True)
        self.general.on_data_changed = self.refresh_all_tables
        self.packages_tab.on_data_changed = self.refresh_all_tables
        self.settings_tab = SettingsTab(tabs.tab("Settings"), self.settings, self.save)
        self.settings_tab.pack(fill="both", expand=True)

    def refresh_all_tables(self) -> None:
        """Reload all data-backed tables after a database mutation."""
        self.general.reload()
        self.packages_tab.load_selected()

    def game_changed(self, game: str) -> None:
        """Apply the global game selection to all game-dependent working tabs."""
        self.settings["selected_game"] = game
        if hasattr(self, "settings_tab"):
            self.settings_tab.settings["selected_game"] = game
        if hasattr(self, "general"):
            self.general.set_game(game)
        if hasattr(self, "packages_tab"):
            self.packages_tab.set_game(game)
        if hasattr(self, "export_maps_tab"):
            self.export_maps_tab.set_game(game)

    def current_settings(self) -> dict:
        """Return current in-memory settings, including unsaved Settings-tab edits when available."""
        return self.settings_tab.values() if hasattr(self, "settings_tab") else self.settings

    def save(self, settings: dict) -> None:
        """Persist validated settings and report the result in the shared styled dialog."""
        try:
            save_settings(settings)
            self.settings = settings
            self.settings_tab.settings = settings
            AppDialog(self, "Settings Saved", "Settings were saved successfully.")
        except (ValueError, OSError) as error:
            AppDialog(self, "Invalid Settings", str(error))
