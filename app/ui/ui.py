"""Main CustomTkinter window and application-level event coordination."""
import threading, customtkinter as ctk
from app.config.config_app import APP_NAME, GITHUB_URL, KOFI_URL
from app.functions.function_links import open_external_url
from app.functions.function_settings import load_settings, save_settings
from app.functions.function_update_check import check_for_update
from app.templates.template_dialog import AppDialog
from app.ui.tabs.ui_tab_general import GeneralTab
from app.ui.tabs.ui_tab_settings import SettingsTab
from app.ui.ui_update_status import UpdateStatusWindow

class MainWindow(ctk.CTk):
    """Own the main window, tabs, settings state, and worker-to-UI handoff."""
    def __init__(self):
        super().__init__(); self.title(APP_NAME); self.geometry("1120x700"); self.minsize(900,560)
        self.settings=load_settings(); self._build(); self.after(250,self._start_update_check)
    def _build(self) -> None:
        """Construct the header and primary tabs."""
        header=ctk.CTkFrame(self); header.pack(fill="x",padx=14,pady=(14,6))
        ctk.CTkLabel(header,text=APP_NAME,font=ctk.CTkFont(size=24,weight="bold")).pack(side="left",padx=14,pady=12)
        ctk.CTkButton(header,text="Ko-fi",width=80,fg_color="#8b4a3b",command=lambda:open_external_url(KOFI_URL)).pack(side="right",padx=(5,14))
        ctk.CTkButton(header,text="GitHub",width=80,fg_color="#24292f",command=lambda:open_external_url(GITHUB_URL)).pack(side="right",padx=5)
        tabs=ctk.CTkTabview(self); tabs.pack(fill="both",expand=True,padx=14,pady=(6,14)); tabs.add("General"); tabs.add("Settings")
        self.general=GeneralTab(tabs.tab("General"),self.settings["selected_game"],self._game_changed); self.general.pack(fill="both",expand=True)
        self.settings_tab=SettingsTab(tabs.tab("Settings"),self.settings,self._save); self.settings_tab.pack(fill="both",expand=True)
    def _game_changed(self, game: str) -> None:
        """Keep the selected database version in application state."""
        self.settings["selected_game"]=game; self.settings_tab.settings["selected_game"]=game
    def _save(self, values: dict) -> None:
        """Validate and save settings, reporting results in styled dialogs."""
        try: save_settings(values); self.settings=values; AppDialog(self,"Settings Saved","Settings were saved successfully.")
        except (ValueError,OSError) as exc: AppDialog(self,"Invalid Settings",str(exc))
    def _start_update_check(self) -> None:
        """Run network access off the UI thread."""
        def worker():
            result=check_for_update(); self.after(0,lambda:UpdateStatusWindow(self,result))
        threading.Thread(target=worker,daemon=True).start()
