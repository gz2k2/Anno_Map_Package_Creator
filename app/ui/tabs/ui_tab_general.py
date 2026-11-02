from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog
from app.config.config_app import SUPPORTED_GAMES
from app.functions.function_database import load_entries,import_map,set_region,delete_maps,assign_map_package,load_packages,package_names,get_package,apply_package_to_maps,change_guid,change_type
from app.templates.template_table import SortableTable
from app.templates.template_dialog import AppDialog,DuplicateDialog,RegionDialog,ConfirmDialog,PackageSelectionDialog,YesNoDialog,GuidDialog,RegionSelectionDialog,TypeSelectionDialog
from app.config.config_regions import get_fixed_regions
class GeneralTab(ctk.CTkFrame):
 def __init__(self,master,selected_game,on_game_changed,get_settings):
  super().__init__(master);self.on_data_changed=lambda:self.reload();self.game_var=ctk.StringVar(value=selected_game);self.on_game_changed=on_game_changed;self.get_settings=get_settings
  filter_bar=ctk.CTkFrame(self,fg_color="transparent");filter_bar.pack(fill="x",padx=18,pady=(0,8));ctk.CTkLabel(filter_bar,text="Filter").pack(side="left",padx=(0,8));self.filter_var=ctk.StringVar(value="All");self.filter_menu=ctk.CTkOptionMenu(filter_bar,values=["All"],variable=self.filter_var,command=lambda _:self.reload());self.filter_menu.pack(side="left")
  actions=ctk.CTkFrame(self,fg_color="transparent");actions.pack(fill="x",padx=18,pady=(0,10));ctk.CTkButton(actions,text="Add Map ( Folder )",command=self.add_folder).pack(side="left",padx=(0,8));ctk.CTkButton(actions,text="Add Map ( File )",command=self.add_file).pack(side="left")
  cols=[("Map_Name","Map Name",190),("Region","Region",120),("Map_Package","Map Package",180),("GUID","GUID",120),("Type","Type",110),("Map_File","Map File",320)];self.table=SortableTable(self,cols);self.table.pack(fill="both",expand=True,padx=18,pady=(0,18));self._build_context_menu();self.reload()
 def _change(self,g):self.on_game_changed(g);self.reload()
 def reload(self):
  packages=sorted(package_names(self.game_var.get()),key=str.casefold);values=["All"]+packages;current=self.filter_var.get() if hasattr(self,"filter_var") else "All"
  if current not in values:current="All";self.filter_var.set("All")
  if hasattr(self,"filter_menu"):self.filter_menu.configure(values=values)
  entries=load_entries(self.game_var.get())
  if current!="All":entries=[e for e in entries if e.map_package==current]
  self.table.set_rows([(e.map_name,e.region,e.map_package,e.guid,e.map_type,e.map_file) for e in entries])
 def _range(self):
  s=self.get_settings();v=s["games"][self.game_var.get()];return v["guid_start"],v["guid_end"]
 def _import(self,path):
  try:
   a,b=self._range();status,_=import_map(self.game_var.get(),path,a,b)
   if status=="duplicate":DuplicateDialog(self,path,lambda:self._update(path))
   else:self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Import Failed",str(e))
 def _update(self,path):
  try:
   a,b=self._range();import_map(self.game_var.get(),path,a,b,True);self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Import Failed",str(e))
 def add_file(self):
  p=filedialog.askopenfilename(parent=self,title="Select Anno Map",filetypes=[("Anno map files","*.a7m"),("All files","*.*")])
  if p:self._import(p)
 def add_folder(self):
  folder=filedialog.askdirectory(parent=self,title="Select Folder Containing Anno Maps")
  if not folder:return
  files=sorted(Path(folder).rglob("*.a7m"),key=lambda p:str(p).casefold())
  if not files:AppDialog(self,"No Maps Found","No .a7m files were found in the selected folder.");return
  for p in files:self._import(str(p))

 def _build_context_menu(self):
  import tkinter as tk
  self.context_menu=tk.Menu(self,tearoff=0,bg="#2b2b2b",fg="#f2f2f2",activebackground="#1f6aa5",activeforeground="#ffffff",bd=0)
  self.context_menu.add_command(label="Set Region",command=self.set_region_for_selection);self.context_menu.add_command(label="Change GUID",command=self.change_guid_selection);self.context_menu.add_command(label="Change Type",command=self.change_type_selection);self.context_menu.add_separator();self.context_menu.add_command(label="Add to Map Package...",command=self.add_to_package);self.context_menu.add_separator();self.context_menu.add_command(label="Delete",command=self.delete_selection)
  self.table.tree.bind("<Button-3>",self._show_context_menu)
 def _show_context_menu(self,event):
  row=self.table.tree.identify_row(event.y)
  if not row:return
  selected=self.table.tree.selection()
  if row not in selected:self.table.tree.selection_set(row)
  self.context_menu.tk_popup(event.x_root,event.y_root)
 def set_region_for_selection(self):
  selected=self.table.tree.selection()
  if not selected:return
  paths=[self.table.tree.set(item,"Map_File") for item in selected]
  RegionSelectionDialog(self,[x["region"] for x in get_fixed_regions(self.game_var.get())],[x.get("region","") for x in self.get_settings()["games"][self.game_var.get()].get("custom_regions",[])],"",lambda region:self._apply_region(paths,region))
 def _apply_region(self,paths,region):
  try:set_region(self.game_var.get(),paths,region.strip());self.on_data_changed()
  except OSError as e:AppDialog(self,"Set Region Failed",str(e))

 def _selected_paths(self):return [self.table.tree.set(i,"Map_File") for i in self.table.tree.selection()]
 def delete_selection(self):
  paths=self._selected_paths()
  if paths:ConfirmDialog(self,"Delete Maps",f"Delete {len(paths)} selected map(s) from the database?",lambda:(delete_maps(self.game_var.get(),paths),self.on_data_changed()))
 def add_to_package(self):
  paths=self._selected_paths();packages=package_names(self.game_var.get())
  if not paths:return
  if not packages:AppDialog(self,"No Map Packages","Create a Map Package in the Map Packages tab first.");return
  PackageSelectionDialog(self,packages,lambda package:self._package_assignment_options(paths,package))
 def _package_assignment_options(self,paths,package):
  pkg=get_package(self.game_var.get(),package)
  def region_step(apply_guids):
   if pkg and pkg["region"]:YesNoDialog(self,"Apply Package Region",f'Apply region "{pkg["region"]}" to the selected map(s)?',lambda:self._finish_package(paths,package,apply_guids,True),lambda:self._finish_package(paths,package,apply_guids,False))
   else:self._finish_package(paths,package,apply_guids,False)
  if pkg and pkg["use_different_guid_ranges"]:YesNoDialog(self,"Apply Package GUID Range",f'Assign new GUIDs from package range {pkg["guid_start"]} to {pkg["guid_end"]}?',lambda:region_step(True),lambda:region_step(False))
  else:region_step(False)
 def _finish_package(self,paths,package,apply_guids,apply_region):
  try:apply_package_to_maps(self.game_var.get(),paths,package,apply_guids,apply_region);self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Map Package",str(e))

 def change_guid_selection(self):
  selected=self.table.tree.selection()
  if len(selected)!=1:
   AppDialog(self,"Change GUID","Change GUID is only available when exactly one map is selected.");return
  item=selected[0];path=self.table.tree.set(item,"Map_File");guid=self.table.tree.set(item,"GUID");GuidDialog(self,guid,lambda value:self._apply_guid(path,value))
 def _apply_guid(self,path,value):
  try:change_guid(self.game_var.get(),path,value);self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Change GUID",str(e))

 def set_game(self,game):
  self.game_var.set(game)
  if hasattr(self,"filter_var"):self.filter_var.set("All")
  self.reload()

 def change_type_selection(self):
  selected=self.table.tree.selection()
  if not selected:return
  paths=[self.table.tree.set(item,"Map_File") for item in selected];current=self.table.tree.set(selected[0],"Type") if len(selected)==1 else "Normal"
  TypeSelectionDialog(self,current,lambda value:self._apply_type(paths,value))
 def _apply_type(self,paths,value):
  try:change_type(self.game_var.get(),paths,value);self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Change Type",str(e))
