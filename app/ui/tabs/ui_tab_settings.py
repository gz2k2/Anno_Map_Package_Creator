"""Settings tab for game-specific GUID ranges and processing options."""
import customtkinter as ctk
from app.config.config_app import SUPPORTED_GAMES

class SettingsTab(ctk.CTkFrame):
    """Collect validated settings while keeping Save fixed bottom-right."""
    def __init__(self, master, settings: dict, save_callback):
        super().__init__(master); self.settings=settings; self.vars={}
        self.grid_rowconfigure(0,weight=1); self.grid_columnconfigure(0,weight=1)
        content=ctk.CTkScrollableFrame(self); content.grid(row=0,column=0,sticky="nsew",padx=18,pady=(18,8))
        validator=(self.register(lambda value: value=="" or value.isdigit()), "%P")
        for game in SUPPORTED_GAMES:
            box=ctk.CTkFrame(content); box.pack(fill="x",pady=8)
            ctk.CTkLabel(box,text=game,font=ctk.CTkFont(size=17,weight="bold")).grid(row=0,column=0,columnspan=2,padx=16,pady=14,sticky="w")
            self.vars[game]={}
            for row,(key,label) in enumerate((("guid_start","GUID Start"),("guid_end","GUID End")),start=1):
                var=ctk.StringVar(value=settings["games"][game][key]); self.vars[game][key]=var
                ctk.CTkLabel(box,text=label).grid(row=row,column=0,padx=16,pady=8,sticky="w")
                ctk.CTkEntry(box,textvariable=var,validate="key",validatecommand=validator).grid(row=row,column=1,padx=16,pady=8,sticky="ew")
            box.grid_columnconfigure(1,weight=1)
        workers=ctk.CTkFrame(content); workers.pack(fill="x",pady=8)
        ctk.CTkLabel(workers,text="Processing",font=ctk.CTkFont(size=17,weight="bold")).grid(row=0,column=0,columnspan=2,padx=16,pady=14,sticky="w")
        self.worker_var=ctk.StringVar(value=str(settings["worker_count"]))
        ctk.CTkLabel(workers,text="Worker Count (1-32)").grid(row=1,column=0,padx=16,pady=8,sticky="w")
        ctk.CTkEntry(workers,textvariable=self.worker_var,validate="key",validatecommand=validator).grid(row=1,column=1,padx=16,pady=8,sticky="ew"); workers.grid_columnconfigure(1,weight=1)
        actions=ctk.CTkFrame(self,fg_color="transparent"); actions.grid(row=1,column=0,sticky="ew",padx=18,pady=(0,18))
        ctk.CTkButton(actions,text="Save",command=lambda: save_callback(self.values())).pack(side="right")
    def values(self) -> dict:
        """Return current UI values in the persisted settings schema."""
        return {"selected_game":self.settings["selected_game"],"worker_count":self.worker_var.get(),"games":{game:{key:var.get() for key,var in values.items()} for game,values in self.vars.items()}}
