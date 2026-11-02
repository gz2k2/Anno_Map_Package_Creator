"""General tab containing game selection and the map database table."""
import customtkinter as ctk
from app.config.config_app import SUPPORTED_GAMES
from app.functions.function_database import load_entries
from app.templates.template_table import SortableTable

class GeneralTab(ctk.CTkFrame):
    """Present the selected game's database in a sortable table."""
    def __init__(self, master, selected_game: str, on_game_changed):
        super().__init__(master)
        self.game_var=ctk.StringVar(value=selected_game); self.on_game_changed=on_game_changed
        header=ctk.CTkFrame(self,fg_color="transparent"); header.pack(fill="x",padx=18,pady=18)
        ctk.CTkLabel(header,text="Database Version",font=ctk.CTkFont(size=16,weight="bold")).pack(side="left")
        ctk.CTkOptionMenu(header,values=list(SUPPORTED_GAMES),variable=self.game_var,command=self._change).pack(side="left",padx=14)
        cols=[("Map_Name","Map Name",200),("Region","Region",130),("Map_Package","Map Package",190),("GUID","GUID",120),("Map_File","Map File",260)]
        self.table=SortableTable(self,cols); self.table.pack(fill="both",expand=True,padx=18,pady=(0,18)); self.reload()
    def _change(self, game: str) -> None:
        """Notify the main window and reload selected database."""
        self.on_game_changed(game); self.reload()
    def reload(self) -> None:
        """Reload rows from the selected JSON database."""
        entries=load_entries(self.game_var.get())
        self.table.set_rows([(e.map_name,e.region,e.map_package,e.guid,e.map_file) for e in entries])
