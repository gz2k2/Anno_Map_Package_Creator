"""Island Database presentation tab. It owns map-list presentation, filtering, context-menu wiring, and user interactions while delegating persistence operations to feature functions."""
import customtkinter as ctk
from app.config.config_app import SUPPORTED_GAMES
from app.functions.function_database import load_entries, set_region, delete_maps, assign_map_package, load_packages, package_names, get_package, apply_package_to_maps, change_guid, change_type, remove_from_package, change_island_size
from app.templates.template_table import SortableTable
from app.templates.template_dialog import AppDialog, RegionDialog, ConfirmDialog, PackageSelectionDialog, YesNoDialog, GuidDialog, RegionSelectionDialog, TypeSelectionDialog, IslandSizeSelectionDialog
from app.config.config_regions import get_fixed_regions

class GeneralTab(ctk.CTkFrame):
  """Represent the GeneralTab component and own its lifecycle within this module."""

  def __init__(self, master, selected_game, on_game_changed, get_settings):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  selected_game: Input used by the init operation.
  on_game_changed: Input used by the init operation.
  get_settings: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.on_data_changed = lambda: self.reload()
      self.game_var = ctk.StringVar(value=selected_game)
      self.on_game_changed = on_game_changed
      self.get_settings = get_settings
      filter_bar = ctk.CTkFrame(self, fg_color='transparent')
      filter_bar.pack(fill='x', padx=18, pady=(0, 10))
      ctk.CTkLabel(filter_bar, text='Filter').pack(side='left', padx=(0, 8))
      self.filter_var = ctk.StringVar(value='All')
      self.filter_menu = ctk.CTkOptionMenu(filter_bar, values=['All'], variable=self.filter_var, command=lambda _: self.reload(), width=220)
      self.filter_menu.pack(side='left')
      cols = [('Map_Name', 'Island Name', 190), ('Region', 'Region', 120), ('Map_Package', 'Island Package', 180), ('GUID', 'GUID', 120), ('Type', 'Type', 110), ('Island_Size', 'Island Size', 110), ('Map_File', 'Map File', 320)]
      self.table = SortableTable(self, cols)
      self.table.pack(fill='both', expand=True, padx=18, pady=(0, 18))
      self._build_context_menu()
      self.reload()

  def _change(self, g):
      """Perform the change operation for this module responsibility.

Args:
  g: Input used by the change operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      self.on_game_changed(g)
      self.reload()

  def reload(self):
      """Perform the reload operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      packages = sorted(package_names(self.game_var.get()), key=str.casefold)
      values = ['All'] + packages
      current = self.filter_var.get() if hasattr(self, 'filter_var') else 'All'
      if current not in values:
          current = 'All'
          self.filter_var.set('All')
      if hasattr(self, 'filter_menu'):
          self.filter_menu.configure(values=values)
      entries = load_entries(self.game_var.get())
      if current != 'All':
          entries = [e for e in entries if e.map_package == current]
      self.table.set_rows([(e.map_name, e.region, e.map_package, e.guid, e.map_type, e.island_size if self.game_var.get() == 'Anno 117' else '', e.map_file) for e in entries])

  def _build_context_menu(self):
      """Perform the build context menu operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      import tkinter as tk
      self.context_menu = tk.Menu(self, tearoff=0, bg='#2b2b2b', fg='#f2f2f2', activebackground='#1f6aa5', activeforeground='#ffffff', bd=0)
      self.context_menu.add_command(label='Set Region', command=self.set_region_for_selection)
      self.context_menu.add_command(label='Change GUID', command=self.change_guid_selection)
      self.context_menu.add_command(label='Change Type', command=self.change_type_selection)
      self.context_menu.add_command(label='Change Island Size', command=self.change_island_size_selection)
      self.context_menu.add_separator()
      self.context_menu.add_command(label='Add to Island Package...', command=self.add_to_package)
      self.context_menu.add_command(label='Remove from Package', command=self.remove_from_package_selection)
      self.context_menu.add_separator()
      self.context_menu.add_command(label='Delete', command=self.delete_selection)
      self.table.tree.bind('<Button-3>', self._show_context_menu)

  def _show_context_menu(self, event):
      """Perform the show context menu operation for this module responsibility.

Args:
  event: Input used by the show context menu operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      row = self.table.tree.identify_row(event.y)
      if not row:
          return
      selected = self.table.tree.selection()
      if row not in selected:
          self.table.tree.selection_set(row)
      self.context_menu.tk_popup(event.x_root, event.y_root)

  def set_region_for_selection(self):
      """Perform the set region for selection operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      selected = self.table.tree.selection()
      if not selected:
          return
      paths = [self.table.tree.set(item, 'Map_File') for item in selected]
      RegionSelectionDialog(self, [x['region'] for x in get_fixed_regions(self.game_var.get())], [x.get('region', '') for x in self.get_settings()['games'][self.game_var.get()].get('custom_regions', [])], '', lambda region: self._apply_region(paths, region))

  def _apply_region(self, paths, region):
      """Perform the apply region operation for this module responsibility.

Args:
  paths: Input used by the apply region operation.
  region: Input used by the apply region operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      try:
          set_region(self.game_var.get(), paths, region.strip())
          self.on_data_changed()
      except OSError as e:
          AppDialog(self, 'Set Region Failed', str(e))

  def _selected_paths(self):
      """Perform the selected paths operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      return [self.table.tree.set(i, 'Map_File') for i in self.table.tree.selection()]

  def delete_selection(self):
      """Perform the delete selection operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      paths = self._selected_paths()
      if paths:
          ConfirmDialog(self, 'Delete Maps', f'Delete {len(paths)} selected map(s) from the database?', lambda: (delete_maps(self.game_var.get(), paths), self.on_data_changed()))

  def add_to_package(self):
      """Perform the add to package operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      paths = self._selected_paths()
      packages = package_names(self.game_var.get())
      if not paths:
          return
      if not packages:
          AppDialog(self, 'No Island Packages', 'Create an Island Package in the Island Packages tab first.')
          return
      PackageSelectionDialog(self, packages, lambda package: self._package_assignment_options(paths, package))

  def _package_assignment_options(self, paths, package):
      """Perform the package assignment options operation for this module responsibility.

Args:
  paths: Input used by the package assignment options operation.
  package: Input used by the package assignment options operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      pkg = get_package(self.game_var.get(), package)

      def region_step(apply_guids):
          """Perform the region step operation for this module responsibility.

Args:
  apply_guids: Input used by the region step operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
          if pkg and pkg['region']:
              YesNoDialog(self, 'Apply Package Region', f'''Apply region "{pkg['region']}" to the selected map(s)?''', lambda: self._finish_package(paths, package, apply_guids, True), lambda: self._finish_package(paths, package, apply_guids, False))
          else:
              self._finish_package(paths, package, apply_guids, False)
      if pkg and pkg['use_different_guid_ranges']:
          YesNoDialog(self, 'Apply Package GUID Range', f"Assign new GUIDs from package range {pkg['guid_start']} to {pkg['guid_end']}?", lambda: region_step(True), lambda: region_step(False))
      else:
          region_step(False)

  def _finish_package(self, paths, package, apply_guids, apply_region):
      """Perform the finish package operation for this module responsibility.

Args:
  paths: Input used by the finish package operation.
  package: Input used by the finish package operation.
  apply_guids: Input used by the finish package operation.
  apply_region: Input used by the finish package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      try:
          apply_package_to_maps(self.game_var.get(), paths, package, apply_guids, apply_region)
          self.on_data_changed()
      except (ValueError, OSError) as e:
          AppDialog(self, 'Map Package', str(e))

  def remove_from_package_selection(self):
      """Remove the selected General-tab maps from their current Map Package."""
      selected = self.table.tree.selection()
      if not selected:
          return
      paths = [self.table.tree.set(item, "Map_File") for item in selected]
      packaged_paths = [
          path
          for item, path in zip(selected, paths)
          if self.table.tree.set(item, "Map_Package").strip()
      ]
      if not packaged_paths:
          AppDialog(self, "Remove from Package", "The selected map(s) are not assigned to a Map Package.")
          return
      ConfirmDialog(
          self,
          "Remove from Package",
          f"Remove {len(packaged_paths)} selected map(s) from their Map Package?",
          lambda: self._remove_from_package(packaged_paths),
          confirm_text="Apply",
          confirm_color=("#3B8ED0", "#1F6AA5"),
      )

  def _remove_from_package(self, paths):
      """Persist removal of selected maps from their Map Package assignments."""
      try:
          changed = remove_from_package(self.game_var.get(), paths)
          self.reload()
          self.on_data_changed()
          AppDialog(self, "Remove from Package", f"Removed {changed} map(s) from their Map Package.")
      except (ValueError, OSError) as error:
          AppDialog(self, "Remove from Package", str(error))

  def change_guid_selection(self):
      """Perform the change guid selection operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      selected = self.table.tree.selection()
      if len(selected) != 1:
          AppDialog(self, 'Change GUID', 'Change GUID is only available when exactly one map is selected.')
          return
      item = selected[0]
      path = self.table.tree.set(item, 'Map_File')
      guid = self.table.tree.set(item, 'GUID')
      GuidDialog(self, guid, lambda value: self._apply_guid(path, value))

  def _apply_guid(self, path, value):
      """Perform the apply guid operation for this module responsibility.

Args:
  path: Input used by the apply guid operation.
  value: Input used by the apply guid operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      try:
          change_guid(self.game_var.get(), path, value)
          self.on_data_changed()
      except (ValueError, OSError) as e:
          AppDialog(self, 'Change GUID', str(e))

  def set_game(self, game):
      """Perform the set game operation for this module responsibility.

Args:
  game: Input used by the set game operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      self.game_var.set(game)
      if hasattr(self, 'filter_var'):
          self.filter_var.set('All')
      self.reload()

  def change_type_selection(self):
      """Perform the change type selection operation for this module responsibility.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      selected = self.table.tree.selection()
      if not selected:
          return
      paths = [self.table.tree.set(item, 'Map_File') for item in selected]
      current = self.table.tree.set(selected[0], 'Type') if len(selected) == 1 else 'Normal'
      TypeSelectionDialog(self, current, lambda value: self._apply_type(paths, value))

  def _apply_type(self, paths, value):
      """Perform the apply type operation for this module responsibility.

Args:
  paths: Input used by the apply type operation.
  value: Input used by the apply type operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      try:
          change_type(self.game_var.get(), paths, value)
          self.on_data_changed()
      except (ValueError, OSError) as e:
          AppDialog(self, 'Change Type', str(e))

  def change_island_size_selection(self):
      """Change Island Size for selected Anno 117 islands."""
      if self.game_var.get() != 'Anno 117':
          AppDialog(self, 'Change Island Size', 'Island Size is only available for Anno 117.')
          return
      selected = self.table.tree.selection()
      if not selected:
          return
      paths = [self.table.tree.set(item, 'Map_File') for item in selected]
      current = self.table.tree.set(selected[0], 'Island_Size') if len(selected) == 1 else 'Auto'
      IslandSizeSelectionDialog(self, current or 'Auto', lambda value: self._apply_island_size(paths, value))

  def _apply_island_size(self, paths, value):
      """Persist Island Size for selected Anno 117 islands and refresh the table."""
      try:
          change_island_size(self.game_var.get(), paths, value)
          self.on_data_changed()
      except (ValueError, OSError) as error:
          AppDialog(self, 'Change Island Size', str(error))
