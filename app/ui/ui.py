import customtkinter as ctk
from app.config.config_app import APP_NAME
from app.functions.function_settings import load_settings,save_settings
from app.templates.template_dialog import AppDialog
from app.ui.tabs.ui_tab_general import GeneralTab
from app.ui.tabs.ui_tab_settings import SettingsTab
from app.ui.tabs.ui_tab_packages import MapPackagesTab
from app.ui.tabs.ui_tab_export_maps import ExportMapsAsModTab
class MainWindow(ctk.CTk):
 def __init__(self):
  super().__init__();self.title(APP_NAME);self.geometry("1120x700");self.settings=load_settings();header=ctk.CTkFrame(self,fg_color="transparent");header.pack(fill="x",padx=14,pady=(14,0));ctk.CTkLabel(header,text="Game",font=ctk.CTkFont(weight="bold")).pack(side="left",padx=(4,10));self.game_toggle=ctk.CTkSegmentedButton(header,values=["Anno 117","Anno 1800"],command=self.game_changed);self.game_toggle.pack(side="left");self.game_toggle.set(self.settings["selected_game"]);tabs=ctk.CTkTabview(self);tabs.pack(fill="both",expand=True,padx=14,pady=(6,14));tabs.add("General");tabs.add("Map Packages");tabs.add("Export Maps as Mod");tabs.add("Settings");self.general=GeneralTab(tabs.tab("General"),self.settings["selected_game"],self.game_changed,self.current_settings);self.general.pack(fill="both",expand=True);self.packages_tab=MapPackagesTab(tabs.tab("Map Packages"));self.packages_tab.pack(fill="both",expand=True);self.export_maps_tab=ExportMapsAsModTab(tabs.tab("Export Maps as Mod"),self.settings["selected_game"]);self.export_maps_tab.pack(fill="both",expand=True);self.general.on_data_changed=self.refresh_all_tables;self.packages_tab.on_data_changed=self.refresh_all_tables;self.settings_tab=SettingsTab(tabs.tab("Settings"),self.settings,self.save);self.settings_tab.pack(fill="both",expand=True)
 def refresh_all_tables(self):
  """Reload every data-backed table after any entry mutation."""
  self.general.reload()
  self.packages_tab.load_selected()

 def game_changed(self,g):
  self.settings["selected_game"]=g
  self.settings_tab.settings["selected_game"]=g
  if hasattr(self,"general"):self.general.set_game(g)
  if hasattr(self,"packages_tab"):self.packages_tab.set_game(g)
  if hasattr(self,"export_maps_tab"):self.export_maps_tab.set_game(g)
 def current_settings(self):return self.settings_tab.values() if hasattr(self,"settings_tab") else self.settings
 def save(self,s):
  try:save_settings(s);self.settings=s;self.settings_tab.settings=s;AppDialog(self,"Settings Saved","Settings were saved successfully.")
  except (ValueError,OSError) as e:AppDialog(self,"Invalid Settings",str(e))
