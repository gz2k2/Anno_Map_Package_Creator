"""Background map-package export UI with live autoscrolling file log."""
from pathlib import Path
from queue import Empty, Queue
import shutil
import threading
import xml.etree.ElementTree as ET
import customtkinter as ctk
from tkinter import filedialog
from app.functions.function_database import get_package, package_entries, package_names
from app.config.config_regions import get_fixed_regions
from app.functions.function_settings import load_settings
from app.templates.template_dialog import AppDialog, ConfirmDialog

class ExportMapsAsModTab(ctk.CTkFrame):
 def __init__(self,master,selected_game):
  super().__init__(master);self.game=ctk.StringVar(value=selected_game);self.map_package=ctk.StringVar();self.mod_name=ctk.StringVar();self.export_folder=ctk.StringVar();self.status=ctk.StringVar(value="Ready");self.messages=Queue();self.worker=None;self._build();self.reload();self.after(75,self._poll)
 def _build(self):
  content=ctk.CTkFrame(self,fg_color="transparent");content.pack(fill="both",expand=True,padx=18,pady=18);content.grid_columnconfigure(1,weight=1);content.grid_rowconfigure(4,weight=1)
  ctk.CTkLabel(content,text="Map Package").grid(row=0,column=0,padx=(0,12),pady=8,sticky="w");self.package_menu=ctk.CTkOptionMenu(content,values=[""],variable=self.map_package);self.package_menu.grid(row=0,column=1,columnspan=2,pady=8,sticky="ew")
  ctk.CTkLabel(content,text="Mod Name").grid(row=1,column=0,padx=(0,12),pady=8,sticky="w");ctk.CTkEntry(content,textvariable=self.mod_name).grid(row=1,column=1,columnspan=2,pady=8,sticky="ew")
  ctk.CTkLabel(content,text="Export Folder").grid(row=2,column=0,padx=(0,12),pady=8,sticky="w");ctk.CTkEntry(content,textvariable=self.export_folder,state="readonly").grid(row=2,column=1,padx=(0,8),pady=8,sticky="ew");ctk.CTkButton(content,text="Browse...",width=100,command=self.select_folder).grid(row=2,column=2,pady=8)
  action=ctk.CTkFrame(content,fg_color="transparent");action.grid(row=3,column=0,columnspan=3,pady=(12,8),sticky="ew");ctk.CTkLabel(action,textvariable=self.status).pack(side="left");self.export_button=ctk.CTkButton(action,text="Export Map Package as Mod",command=self.export);self.export_button.pack(side="right")
  frame=ctk.CTkFrame(content);frame.grid(row=4,column=0,columnspan=3,sticky="nsew");frame.grid_columnconfigure(0,weight=1);frame.grid_rowconfigure(1,weight=1);ctk.CTkLabel(frame,text="Export Log",font=ctk.CTkFont(weight="bold")).grid(row=0,column=0,padx=12,pady=8,sticky="w");self.log=ctk.CTkTextbox(frame,state="disabled",wrap="none");self.log.grid(row=1,column=0,padx=10,pady=(0,10),sticky="nsew")
 def reload(self):
  values=sorted(package_names(self.game.get()),key=str.casefold);current=self.map_package.get();self.package_menu.configure(values=values or [""]);self.map_package.set(current if current in values else (values[0] if values else ""))
 def set_game(self,game):self.game.set(game);self.reload()
 def select_folder(self):
  value=filedialog.askdirectory(parent=self,title="Select Export Folder",initialdir=self.export_folder.get() or None)
  if value:self.export_folder.set(value)
 def export(self):
  if self.worker and self.worker.is_alive():return
  package=self.map_package.get().strip();name=self.mod_name.get().strip();root=self.export_folder.get().strip()
  if not package:AppDialog(self,"Export Failed","Select a Map Package first.");return
  if not name:AppDialog(self,"Export Failed","Mod Name must not be empty.");return
  if any(c in name for c in '<>:"/\\|?*'):AppDialog(self,"Export Failed","Mod Name contains invalid Windows filename characters.");return
  if not root or not Path(root).is_dir():AppDialog(self,"Export Failed","Select an existing Export Folder first.");return
  entries=package_entries(self.game.get(),package)
  if not entries:AppDialog(self,"Export Failed","The selected Map Package does not contain any maps.");return
  pkg=get_package(self.game.get(),package)
  if not pkg or not pkg.get("id"):AppDialog(self,"Export Failed","The selected Map Package has no internal ID.");return
  package_id=pkg["id"]
  target=Path(root)/f"[MapPackage] {name}"
  if target.exists():ConfirmDialog(self,"Replace Existing Mod",f'The folder "{target.name}" already exists. Replace it?',lambda:self._start(target,entries,package_id))
  else:self._start(target,entries,package_id)
 def _start(self,target,entries,package_id):
  self._clear();self.export_button.configure(state="disabled");self.status.set("Exporting...");self._write(f"Target: {target}");self.worker=threading.Thread(target=self._work,args=(target,list(entries),package_id,self.game.get()),daemon=True);self.worker.start()
 def _work(self,target,entries,package_id,game):
  try:
   folders=[];seen=set()
   for entry in entries:
    file=Path(entry.map_file)
    if not file.is_file():raise FileNotFoundError(f"Map file not found: {file}")
    folder=file.parent.resolve();key=str(folder).casefold()
    if key not in seen:seen.add(key);folders.append(folder)
   if target.exists():self.messages.put(("log",f"Removing existing folder: {target}"));shutil.rmtree(target)
   islands_root=target/"data"/package_id/"islands";islands_root.mkdir(parents=True);self.messages.put(("log",f"Islands folder: {islands_root}"));names=set();count=0
   for folder in folders:
    if folder.name.casefold() in names:raise ValueError(f"Multiple map folders use the same folder name: {folder.name}")
    names.add(folder.name.casefold());destination=islands_root/folder.name;self.messages.put(("log",f"Copy folder: {folder} -> {destination}"))
    for source in folder.rglob("*"):
     output=destination/source.relative_to(folder)
     if source.is_dir():output.mkdir(parents=True,exist_ok=True)
     else:output.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,output);count+=1;self.messages.put(("log",f"Copied: {source} -> {output}"))
   if game == "Anno 1800":
    assets_path=self._write_assets_xml(target,entries,package_id,game)
    self.messages.put(("log",f"Created: {assets_path}"))
   else:
    self.messages.put(("log","Skipped assets.xml: Anno 1800 templates are not used for Anno 117."))
   self.messages.put(("done",(target,len(folders),count)))
  except Exception as error:self.messages.put(("error",str(error)))
 def _write_assets_xml(self,target,entries,package_id,game):
  assets_dir=target/"data"/"config"/"export"/"main"/"asset";assets_dir.mkdir(parents=True,exist_ok=True);assets_path=assets_dir/"assets.xml"
  region_map={item["region"]:str(item.get("id","")).strip() for item in get_fixed_regions(game)}
  settings=load_settings()
  for item in settings.get("games",{}).get(game,{}).get("custom_regions",[]):region_map[str(item.get("region",""))]=str(item.get("id","")).strip()
  root=ET.Element("ModOps");root.append(ET.Comment(" START ADDING NEW ISLANDS TO ISLAND POOL "));modop=ET.SubElement(root,"ModOp",{"GUID":"116676","Type":"addNextSibling"})
  for entry in entries:
   map_file=Path(entry.map_file);relative=f"data/{package_id}/islands/{map_file.parent.name}/{map_file.name}";modop.append(ET.Comment(f" {entry.map_name} "));asset=ET.SubElement(modop,"Asset");ET.SubElement(asset,"Template").text="RandomIsland";values=ET.SubElement(asset,"Values");standard=ET.SubElement(values,"Standard");ET.SubElement(standard,"GUID").text=str(entry.guid);ET.SubElement(standard,"Name").text=entry.map_name;random_island=ET.SubElement(values,"RandomIsland");ET.SubElement(random_island,"FilePath").text=relative;mapped_region=region_map.get(entry.region,"")
   if not mapped_region:raise ValueError(f'No Region ID mapping found for "{entry.region}" in {game}.')
   ET.SubElement(random_island,"IslandRegion").text=mapped_region;ET.SubElement(random_island,"IslandDifficulty").text="Normal;Hard"
   if entry.map_type=="Decoration":ET.SubElement(random_island,"IslandType").text="Decoration"
   else:
    ET.SubElement(random_island,"IslandType").text="Normal;Starter";ET.SubElement(random_island,"IslandBaseName").text=entry.map_name
  root.append(ET.Comment(" END ADDING NEW ISLANDS TO ISLAND POOL "));tree=ET.ElementTree(root);ET.indent(tree,space="  ");tree.write(assets_path,encoding="utf-8",xml_declaration=False,short_empty_elements=False);return assets_path
 def _poll(self):
  try:
   while True:
    kind,payload=self.messages.get_nowait()
    if kind=="log":self._write(payload)
    elif kind=="done":
     target,folders,files=payload;self._write(f"Complete: {folders} folder(s), {files} file(s).");self.status.set("Export complete");self.export_button.configure(state="normal");AppDialog(self,"Export Complete",f"Exported {folders} map folder(s) and {files} file(s) to:\n{target}")
    elif kind=="error":self._write(f"ERROR: {payload}");self.status.set("Export failed");self.export_button.configure(state="normal");AppDialog(self,"Export Failed",payload)
  except Empty:pass
  self.after(75,self._poll)
 def _write(self,text):self.log.configure(state="normal");self.log.insert("end",text+"\n");self.log.see("end");self.log.configure(state="disabled")
 def _clear(self):self.log.configure(state="normal");self.log.delete("1.0","end");self.log.configure(state="disabled")
