import customtkinter as ctk
from app.config.config_app import SUPPORTED_GAMES
from app.config.config_regions import get_fixed_regions
from app.functions.function_database import load_packages,package_names,package_entries,add_package,rename_package,delete_package,update_package_options,remove_from_package,change_guid,change_type,set_region
from app.templates.template_dialog import TextInputDialog,ConfirmDialog,AppDialog,GuidDialog,RegionSelectionDialog,TypeSelectionDialog
from app.templates.template_table import SortableTable
from app.ui.ui_dialog_additional_files import AdditionalFilesDialog
class MapPackagesTab(ctk.CTkFrame):
 def __init__(self,master,selected_game="Anno 117"):
  super().__init__(master);self.on_data_changed=lambda:self.load_selected();self.game=ctk.StringVar(value=selected_game);self.package=ctk.StringVar();self.mod_name=ctk.StringVar();self.version=ctk.StringVar();self.region=ctk.StringVar();self.use_range=ctk.BooleanVar();self.guid_start=ctk.StringVar();self.guid_end=ctk.StringVar();self._build();self.reload()
 def _build(self):
  top=ctk.CTkFrame(self,fg_color="transparent");top.pack(fill="x",padx=18,pady=(18,8));ctk.CTkLabel(top,text="Map Package").pack(side="left",padx=(20,8));self.menu=ctk.CTkOptionMenu(top,values=[""],variable=self.package,command=lambda _:self.load_selected());self.menu.pack(side="left");self.menu.configure(width=220);ctk.CTkButton(top,text="New",width=75,command=self.new).pack(side="left",padx=(10,4));ctk.CTkButton(top,text="Rename",width=75,command=self.rename).pack(side="left",padx=4);ctk.CTkButton(top,text="Delete",width=75,fg_color="#b33a3a",command=self.delete).pack(side="left",padx=4)
  opts=ctk.CTkFrame(self);opts.pack(fill="x",padx=18,pady=8);ctk.CTkLabel(opts,text="Mod Name").grid(row=0,column=0,padx=14,pady=10,sticky="w");ctk.CTkEntry(opts,textvariable=self.mod_name,width=220).grid(row=0,column=1,padx=8,pady=10,sticky="w");ctk.CTkButton(opts,text="Additional Files",command=self.open_additional_files).grid(row=0,column=2,padx=(14,18),pady=10,sticky="e");self.additional_files_info=ctk.CTkLabel(opts,text="",text_color="#a0a0a0",font=ctk.CTkFont(size=11));self.additional_files_info.grid(row=1,column=2,padx=(14,18),pady=(0,6),sticky="e");ctk.CTkLabel(opts,text="Version").grid(row=1,column=0,padx=14,pady=10,sticky="w");ctk.CTkEntry(opts,textvariable=self.version,width=220).grid(row=1,column=1,padx=8,pady=10,sticky="w");ctk.CTkLabel(opts,text="Region").grid(row=2,column=0,padx=14,pady=10,sticky="w");self.region_menu=ctk.CTkOptionMenu(opts,values=[""],variable=self.region,command=self._region_selected);self.region_menu.grid(row=2,column=1,padx=8,pady=10,sticky="w");self.region_menu.configure(width=220);ctk.CTkCheckBox(opts,text="Use different GUID ranges",variable=self.use_range,command=self.toggle_range).grid(row=3,column=0,columnspan=2,padx=14,pady=10,sticky="w");self.range_frame=ctk.CTkFrame(opts,fg_color="transparent");ctk.CTkLabel(self.range_frame,text="GUID Start").pack(side="left");ctk.CTkEntry(self.range_frame,textvariable=self.guid_start,width=180).pack(side="left",padx=(8,18));ctk.CTkLabel(self.range_frame,text="GUID End").pack(side="left");ctk.CTkEntry(self.range_frame,textvariable=self.guid_end,width=180).pack(side="left",padx=8);ctk.CTkButton(opts,text="Save Package Settings",command=self.save_options).grid(row=2,column=2,padx=(14,18),pady=10,sticky="e");opts.grid_columnconfigure(1,weight=0);opts.grid_columnconfigure(2,weight=1)
  cols=[("Map_Name","Map Name",180),("Region","Region",120),("Map_Package","Map Package",170),("GUID","GUID",110),("Type","Type",110),("Map_File","Map File",300)];self.table=SortableTable(self,cols);self.table.pack(fill="both",expand=True,padx=18,pady=(4,18));self._build_context_menu()
 def open_additional_files(self):
  if not self.package.get():AppDialog(self,"Additional Files","Select a Map Package first.");return
  AdditionalFilesDialog(self,self.game.get(),self.package.get(),self.on_data_changed)
 def toggle_range(self):
  if self.use_range.get():self.range_frame.grid(row=4,column=0,columnspan=3,padx=14,pady=(0,12),sticky="w")
  else:self.range_frame.grid_remove()
 def reload(self):
  vals=sorted(package_names(self.game.get()), key=str.casefold);self.menu.configure(values=vals or [""]);self.package.set(vals[0] if vals else "");self.load_selected()
 def load_selected(self):
  root=self.winfo_toplevel();settings=root.current_settings() if hasattr(root,"settings_tab") else getattr(root,"settings",{"games":{}});fixed=sorted([x["region"] for x in get_fixed_regions(self.game.get())],key=str.casefold);custom=sorted([x.get("region","") for x in settings.get("games",{}).get(self.game.get(),{}).get("custom_regions",[]) if x.get("region","")],key=str.casefold);region_values=fixed+(["──────── Custom Regions ────────"] if custom else [])+custom
  if hasattr(self,"region_menu"):self.region_menu.configure(values=region_values or [""])
  pkg=next((x for x in load_packages(self.game.get()) if x["name"]==self.package.get()),None)
  if pkg:self.mod_name.set(pkg.get("mod_name",""));self.version.set(pkg.get("version",""));self.region.set(pkg["region"]);self.use_range.set(pkg["use_different_guid_ranges"]);self.guid_start.set(pkg["guid_start"]);self.guid_end.set(pkg["guid_end"]);self.additional_files_info.configure(text=f"{len(pkg.get('additional_files', []))} additional file folder(s)" if pkg.get("additional_files") else "")
  else:self.mod_name.set("");self.version.set("");self.region.set("");self.use_range.set(False);self.guid_start.set("");self.guid_end.set("");self.additional_files_info.configure(text="")
  self.toggle_range();rows=package_entries(self.game.get(),self.package.get());self.table.set_rows([(e.map_name,e.region,e.map_package,e.guid,e.map_type,e.map_file) for e in rows])
 def safe(self,fn):
  try:fn();self.reload();self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Map Package",str(e))
 def save_options(self):
  try:update_package_options(self.game.get(),self.package.get(),self.mod_name.get(),self.version.get(),self.region.get(),self.use_range.get(),self.guid_start.get(),self.guid_end.get());self.on_data_changed();AppDialog(self,"Map Package","Package settings saved.")
  except (ValueError,OSError) as e:AppDialog(self,"Map Package",str(e))
 def new(self):TextInputDialog(self,"New Map Package","Name",self._add_and_select)
 def _add_and_select(self,name):
  try:add_package(self.game.get(),name);self.reload();self.package.set(name.strip());self.load_selected();self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Map Package",str(e))
 def rename(self):
  old=self.package.get()
  if old:TextInputDialog(self,"Rename Map Package","New name",lambda n:self.safe(lambda:rename_package(self.game.get(),old,n)),old)
 def delete(self):
  n=self.package.get()
  if n:ConfirmDialog(self,"Delete Map Package",f'Delete "{n}"? Existing map assignments will be cleared.',lambda:self.safe(lambda:delete_package(self.game.get(),n)))

 def _build_context_menu(self):
  import tkinter as tk
  self.context_menu=tk.Menu(self,tearoff=0,bg="#2b2b2b",fg="#f2f2f2",activebackground="#1f6aa5",activeforeground="#ffffff",bd=0)
  self.context_menu.add_command(label="Set Region",command=self.set_region_for_selection)
  self.context_menu.add_command(label="Change GUID",command=self.change_guid_selection)
  self.context_menu.add_command(label="Change Type",command=self.change_type_selection)
  self.context_menu.add_separator()
  self.context_menu.add_command(label="Remove from Package",command=self.remove_selection)
  self.table.tree.bind("<Button-3>",self._show_context_menu)
 def _show_context_menu(self,event):
  row=self.table.tree.identify_row(event.y)
  if not row:return
  if row not in self.table.tree.selection():self.table.tree.selection_set(row)
  self.context_menu.tk_popup(event.x_root,event.y_root)
 def _selected_paths(self):return [self.table.tree.set(i,"Map_File") for i in self.table.tree.selection()]
 def set_region_for_selection(self):
  selected=self.table.tree.selection()
  if not selected:return
  paths=[self.table.tree.set(item,"Map_File") for item in selected]
  RegionSelectionDialog(self,[x["region"] for x in get_fixed_regions(self.game.get())],[],"",lambda region:self._apply_region(paths,region))
 def _apply_region(self,paths,region):
  try:set_region(self.game.get(),paths,region.strip());self.on_data_changed()
  except OSError as e:AppDialog(self,"Set Region Failed",str(e))
 def remove_selection(self):
  paths=self._selected_paths()
  if paths:ConfirmDialog(self,"Remove from Package",f"Remove {len(paths)} selected map(s) from this package?",lambda:(remove_from_package(self.game.get(),paths),self.on_data_changed()))
 def change_guid_selection(self):
  selected=self.table.tree.selection()
  if len(selected)!=1:
   AppDialog(self,"Change GUID","Change GUID is only available when exactly one map is selected.");return
  item=selected[0];path=self.table.tree.set(item,"Map_File");guid=self.table.tree.set(item,"GUID");GuidDialog(self,guid,lambda value:self._apply_guid(path,value))
 def _apply_guid(self,path,value):
  try:change_guid(self.game.get(),path,value);self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Change GUID",str(e))

 def _region_selected(self,value):
  if value.startswith("─"):
   pkg=next((x for x in load_packages(self.game.get()) if x["name"]==self.package.get()),None)
   self.region.set(pkg.get("region","") if pkg else "")
 def set_game(self,game):
  self.game.set(game)
  self.reload()


 def change_type_selection(self):
  selected=self.table.tree.selection()
  if not selected:return
  paths=[self.table.tree.set(item,"Map_File") for item in selected];current=self.table.tree.set(selected[0],"Type") if len(selected)==1 else "Normal"
  TypeSelectionDialog(self,current,lambda value:self._apply_type(paths,value))
 def _apply_type(self,paths,value):
  try:change_type(self.game.get(),paths,value);self.on_data_changed()
  except (ValueError,OSError) as e:AppDialog(self,"Change Type",str(e))
