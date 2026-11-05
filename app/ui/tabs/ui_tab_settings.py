"""Settings tab presentation. It owns settings widgets, game-specific sub-tabs, custom-region table interactions, and collection of values for persistence by the owning main window."""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from app.config.config_app import SUPPORTED_GAMES
from app.functions.function_settings import save_custom_regions
from app.templates.template_table import SortableTable
from app.templates.template_dialog import TextInputDialog, ConfirmDialog, AppDialog

class SettingsTab(ctk.CTkFrame):
    """Represent the SettingsTab component and own its lifecycle within this module."""

    def __init__(self, master, settings, save):
        """Perform the init operation for this module responsibility.

Args:
    master: Input used by the init operation.
    settings: Input used by the init operation.
    save: Input used by the init operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        super().__init__(master)
        self.settings = settings
        self.save_callback = save
        self.vars = {}
        self.region_tables = {}
        self.region_menus = {}
        self.region_vars = {}
        self.region_id_vars = {}
        self.creator_var = ctk.StringVar(value=settings.get('creator', ''))
        self.creator_url_var = ctk.StringVar(value=settings.get('creator_url', ''))
        self._build()

    def _build(self):
        """Perform the build operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill='both', expand=True, padx=12, pady=(12, 6))
        for name in ('General', 'Anno 117', 'Anno 1800'):
            self.tabs.add(name)
        self._build_general(self.tabs.tab('General'))
        for game in SUPPORTED_GAMES:
            self._build_game(self.tabs.tab(game), game)
        self.save_button = ctk.CTkButton(self, text='Save', command=lambda: self.save_callback(self.values()))
        self.save_button.pack(anchor='e', padx=18, pady=(0, 18))

    def _build_general(self, parent):
        """Perform the build general operation for this module responsibility.

Args:
    parent: Input used by the build general operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        box = ctk.CTkFrame(parent)
        box.pack(fill='x', padx=14, pady=14)
        box.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(box, text='General Settings', font=ctk.CTkFont(size=18, weight='bold')).grid(row=0, column=0, columnspan=2, padx=16, pady=(16, 10), sticky='w')
        ctk.CTkLabel(box, text='Creator').grid(row=1, column=0, padx=(16, 10), pady=8, sticky='w')
        ctk.CTkEntry(box, textvariable=self.creator_var, width=220).grid(row=1, column=1, padx=(0, 16), pady=8, sticky='w')
        ctk.CTkLabel(box, text='Creator Contact').grid(row=2, column=0, padx=(16, 10), pady=(8, 16), sticky='w')
        ctk.CTkEntry(box, textvariable=self.creator_url_var, width=220).grid(row=2, column=1, padx=(0, 16), pady=(8, 16), sticky='w')

    def _build_game(self, parent, game):
        """Perform the build game operation for this module responsibility.

Args:
    parent: Input used by the build game operation.
    game: Input used by the build game operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        validator = (self.register(lambda x: x == '' or x.isdigit()), '%P')
        self.vars[game] = {}
        guid = ctk.CTkFrame(parent)
        guid.pack(fill='x', padx=14, pady=(14, 8))
        ctk.CTkLabel(guid, text='GUID Range', font=ctk.CTkFont(size=17, weight='bold')).grid(row=0, column=0, columnspan=4, padx=14, pady=12, sticky='w')
        for col, (key, label) in enumerate((('guid_start', 'GUID Start'), ('guid_end', 'GUID End'))):
            var = ctk.StringVar(value=self.settings['games'][game][key])
            self.vars[game][key] = var
            ctk.CTkLabel(guid, text=label).grid(row=1, column=col * 2, padx=(14, 6), pady=10, sticky='w')
            ctk.CTkEntry(guid, textvariable=var, validate='key', validatecommand=validator, width=140).grid(row=1, column=col * 2 + 1, padx=(0, 14), pady=10, sticky='ew')
        guid.grid_columnconfigure(1, weight=0)
        guid.grid_columnconfigure(3, weight=0)
        export_var = ctk.StringVar(value=self.settings['games'][game].get('default_export_path', ''))
        self.vars[game]['default_export_path'] = export_var
        ctk.CTkLabel(guid, text='Default Export Path').grid(row=2, column=0, padx=14, pady=10, sticky='w')
        ctk.CTkEntry(guid, textvariable=export_var, width=420).grid(row=2, column=1, columnspan=2, padx=(0, 8), pady=10, sticky='w')
        ctk.CTkButton(guid, text='Browse...', width=90, command=lambda g=game: self.select_export_path(g)).grid(row=2, column=3, padx=(0, 14), pady=10, sticky='e')
        region = ctk.CTkFrame(parent)
        region.pack(fill='both', expand=True, padx=14, pady=8)
        top = ctk.CTkFrame(region, fg_color='transparent')
        top.pack(fill='x', padx=12, pady=12)
        ctk.CTkLabel(top, text='Custom Region', font=ctk.CTkFont(size=17, weight='bold')).grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky='w')
        ctk.CTkLabel(top, text='Region:').grid(row=1, column=0, padx=(0, 6), sticky='w')
        region_var = ctk.StringVar()
        id_var = ctk.StringVar()
        self.region_vars[game] = region_var
        self.region_id_vars[game] = id_var
        ctk.CTkEntry(top, textvariable=region_var, width=220).grid(row=1, column=1, padx=(0, 14), sticky='w')
        ctk.CTkLabel(top, text='ID:').grid(row=1, column=2, padx=(0, 6), sticky='w')
        ctk.CTkEntry(top, textvariable=id_var, width=220).grid(row=1, column=3, padx=(0, 14), sticky='w')
        ctk.CTkButton(top, text='Add', width=80, command=lambda g=game: self.add_from_fields(g)).grid(row=1, column=4)
        top.grid_columnconfigure(1, weight=0)
        top.grid_columnconfigure(3, weight=0)
        table = SortableTable(region, [('Region', 'Region', 220), ('ID', 'ID', 160)])
        table.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        self.region_tables[game] = table
        self._bind_region_context_menu(game, table)
        self.reload_custom_regions(game)

    def select_export_path(self, game):
        """Perform the select export path operation for this module responsibility.

Args:
    game: Input used by the select export path operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        value = filedialog.askdirectory(parent=self, title=f'Select Default Export Path - {game}', initialdir=self.vars[game]['default_export_path'].get() or None)
        if value:
            self.vars[game]['default_export_path'].set(value)

    def regions(self, game):
        """Perform the regions operation for this module responsibility.

Args:
    game: Input used by the regions operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        return self.settings['games'][game].setdefault('custom_regions', [])

    def reload_custom_regions(self, game):
        """Perform the reload custom regions operation for this module responsibility.

Args:
    game: Input used by the reload custom regions operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        regions = sorted(self.regions(game), key=lambda x: x.get('region', '').casefold())
        self.region_tables[game].set_rows([(x.get('region', ''), x.get('id', '')) for x in regions])

    def add_from_fields(self, game):
        """Perform the add from fields operation for this module responsibility.

Args:
    game: Input used by the add from fields operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        name = self.region_vars[game].get().strip()
        ident = self.region_id_vars[game].get().strip()
        if not name:
            AppDialog(self, 'Custom Region', 'Region must not be empty.')
            return
        if any((x.get('region', '').casefold() == name.casefold() for x in self.regions(game))):
            AppDialog(self, 'Custom Region', 'This region already exists.')
            return
        self.regions(game).append({'region': name, 'id': ident})
        save_custom_regions(game, self.regions(game))
        self.region_vars[game].set('')
        self.region_id_vars[game].set('')
        self.reload_custom_regions(game)

    def new_region(self, game):
        """Perform the new region operation for this module responsibility.

Args:
    game: Input used by the new region operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        TextInputDialog(self, 'New Custom Region', 'Region name', lambda name: self.ask_id(game, name))

    def rename_selected_region(self, game):
        """Perform the rename selected region operation for this module responsibility.

Args:
    game: Input used by the rename selected region operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        old = self.region_vars[game].get()
        if old:
            TextInputDialog(self, 'Rename Custom Region', 'New region name', lambda name: self.rename_region(game, old, name), old)
        else:
            AppDialog(self, 'Custom Region', 'Create or select a custom region first.')

    def delete_selected_region(self, game):
        """Perform the delete selected region operation for this module responsibility.

Args:
    game: Input used by the delete selected region operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        name = self.region_vars[game].get()
        if name:
            ConfirmDialog(self, 'Delete Custom Region', f'Delete custom region "{name}"?', lambda: self.delete_region(game, name))
        else:
            AppDialog(self, 'Custom Region', 'Create or select a custom region first.')

    def ask_id(self, game, name):
        """Perform the ask id operation for this module responsibility.

Args:
    game: Input used by the ask id operation.
    name: Input used by the ask id operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        TextInputDialog(self, 'Custom Region ID', 'ID', lambda ident: self.add_region(game, name, ident))

    def add_region(self, game, name, ident):
        """Perform the add region operation for this module responsibility.

Args:
    game: Input used by the add region operation.
    name: Input used by the add region operation.
    ident: Input used by the add region operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        name = name.strip()
        ident = ident.strip()
        if not name:
            return
        if any((x['region'].casefold() == name.casefold() for x in self.regions(game))):
            AppDialog(self, 'Custom Region', 'This region already exists.')
            return
        self.regions(game).append({'region': name, 'id': ident})
        save_custom_regions(game, self.regions(game))
        self.region_vars[game].set(name)
        self.reload_custom_regions(game)

    def rename_region(self, game, old, new):
        """Perform the rename region operation for this module responsibility.

Args:
    game: Input used by the rename region operation.
    old: Input used by the rename region operation.
    new: Input used by the rename region operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        new = new.strip()
        if not new:
            return
        if any((x['region'].casefold() == new.casefold() and x['region'] != old for x in self.regions(game))):
            AppDialog(self, 'Custom Region', 'This region already exists.')
            return
        for x in self.regions(game):
            if x['region'] == old:
                x['region'] = new
        save_custom_regions(game, self.regions(game))
        self.region_vars[game].set(new)
        self.reload_custom_regions(game)

    def delete_region(self, game, name):
        """Perform the delete region operation for this module responsibility.

Args:
    game: Input used by the delete region operation.
    name: Input used by the delete region operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        self.settings['games'][game]['custom_regions'] = [x for x in self.regions(game) if x['region'] != name]
        save_custom_regions(game, self.regions(game))
        self.reload_custom_regions(game)

    def _bind_region_context_menu(self, game, table):
        """Perform the bind region context menu operation for this module responsibility.

Args:
    game: Input used by the bind region context menu operation.
    table: Input used by the bind region context menu operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        menu = tk.Menu(self, tearoff=0, bg='#2b2b2b', fg='#f2f2f2', activebackground='#1f6aa5', activeforeground='#ffffff', bd=0)
        menu.add_command(label='Change Region', command=lambda g=game: self.change_region_name(g))
        menu.add_command(label='Change ID', command=lambda g=game: self.change_region_id(g))
        menu.add_separator()
        menu.add_command(label='Delete', command=lambda g=game: self.delete_region_from_table(g))

        def show(event):
            """Perform the show operation for this module responsibility.

Args:
    event: Input used by the show operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
            row = table.tree.identify_row(event.y)
            if not row:
                return
            if row not in table.tree.selection():
                table.tree.selection_set(row)
            menu.tk_popup(event.x_root, event.y_root)
        table.tree.bind('<Button-3>', show)

    def change_region_name(self, game):
        """Perform the change region name operation for this module responsibility.

Args:
    game: Input used by the change region name operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        tree = self.region_tables[game].tree
        selected = tree.selection()
        if len(selected) != 1:
            AppDialog(self, 'Change Region', 'Change Region is only available when exactly one custom region is selected.')
            return
        old = tree.set(selected[0], 'Region')
        TextInputDialog(self, 'Change Region', 'Region', lambda value: self._apply_region_name(game, old, value), old)

    def _apply_region_name(self, game, old, new):
        """Perform the apply region name operation for this module responsibility.

Args:
    game: Input used by the apply region name operation.
    old: Input used by the apply region name operation.
    new: Input used by the apply region name operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        new = new.strip()
        if not new:
            return
        if any((x.get('region', '').casefold() == new.casefold() and x.get('region') != old for x in self.regions(game))):
            AppDialog(self, 'Custom Region', 'This region already exists.')
            return
        for item in self.regions(game):
            if item.get('region') == old:
                item['region'] = new
                break
        save_custom_regions(game, self.regions(game))
        self.reload_custom_regions(game)

    def delete_region_from_table(self, game):
        """Perform the delete region from table operation for this module responsibility.

Args:
    game: Input used by the delete region from table operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        tree = self.region_tables[game].tree
        selected = tree.selection()
        if len(selected) != 1:
            AppDialog(self, 'Delete Custom Region', 'Delete is only available when exactly one custom region is selected.')
            return
        name = tree.set(selected[0], 'Region')
        ConfirmDialog(self, 'Delete Custom Region', f'Delete custom region "{name}"?', lambda: self.delete_region(game, name))

    def change_region_id(self, game):
        """Perform the change region id operation for this module responsibility.

Args:
    game: Input used by the change region id operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        tree = self.region_tables[game].tree
        selected = tree.selection()
        if len(selected) != 1:
            AppDialog(self, 'Change ID', 'Change ID is only available when exactly one custom region is selected.')
            return
        region = tree.set(selected[0], 'Region')
        current = tree.set(selected[0], 'ID')
        TextInputDialog(self, 'Change ID', f'ID for "{region}"', lambda value: self._apply_region_id(game, region, value), current)

    def _apply_region_id(self, game, region, new_id):
        """Perform the apply region id operation for this module responsibility.

Args:
    game: Input used by the apply region id operation.
    region: Input used by the apply region id operation.
    new_id: Input used by the apply region id operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        for item in self.regions(game):
            if item.get('region') == region:
                item['id'] = new_id.strip()
                break
        save_custom_regions(game, self.regions(game))
        self.reload_custom_regions(game)

    def values(self):
        """Perform the values operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        self.settings['creator'] = self.creator_var.get().strip()
        self.settings['creator_url'] = self.creator_url_var.get().strip()
        for game in SUPPORTED_GAMES:
            self.settings['games'][game]['guid_start'] = self.vars[game]['guid_start'].get()
            self.settings['games'][game]['guid_end'] = self.vars[game]['guid_end'].get()
            self.settings['games'][game]['default_export_path'] = self.vars[game]['default_export_path'].get()
        return self.settings
