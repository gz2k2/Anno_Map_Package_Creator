"""Reusable CustomTkinter dialog components. The module centralizes modal lifecycle and common prompt patterns so feature UI modules remain focused on feature-specific callbacks."""
import customtkinter as ctk

def _close_then(dialog, callback):
  """Close a CTk dialog first, then run its callback from the owning window."""
  owner = dialog.master
  dialog.grab_release()
  dialog.withdraw()
  dialog.after_idle(dialog.destroy)
  owner.after_idle(callback)

class AppDialog(ctk.CTkToplevel):
  """Represent the AppDialog component and own its lifecycle within this module."""

  def __init__(self, master, title, message):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  title: Input used by the init operation.
  message: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title(title)
      self.geometry('520x220')
      self.transient(master)
      self.grab_set()
      ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text=message, wraplength=470, justify='left').pack(padx=24, pady=8, anchor='w')
      ctk.CTkButton(self, text='Close', command=self.destroy).pack(padx=24, pady=20, anchor='e')

class DuplicateDialog(ctk.CTkToplevel):
  """Represent the DuplicateDialog component and own its lifecycle within this module."""

  def __init__(self, master, path, callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  path: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title('Duplicate Map')
      self.geometry('560x240')
      self.transient(master)
      self.grab_set()
      ctk.CTkLabel(self, text='Map already exists', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text=f'The following map is already in the database:\n{path}\n\nUpdate the existing entry or keep it unchanged?', wraplength=510, justify='left').pack(padx=24, anchor='w')
      bar = ctk.CTkFrame(self, fg_color='transparent')
      bar.pack(fill='x', padx=24, pady=22)
      ctk.CTkButton(bar, text='Keep', fg_color='#555', command=self.destroy).pack(side='right', padx=(8, 0))
      ctk.CTkButton(bar, text='Update', command=lambda: _close_then(self, callback)).pack(side='right')

class RegionDialog(ctk.CTkToplevel):
  """Represent the RegionDialog component and own its lifecycle within this module."""

  def __init__(self, master, count, callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  count: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title('Set Region')
      self.geometry('460x210')
      self.transient(master)
      self.grab_set()
      self.var = ctk.StringVar()
      ctk.CTkLabel(self, text='Set Region', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text=f'Region name for {count} selected map(s):').pack(padx=24, pady=(0, 8), anchor='w')
      entry = ctk.CTkEntry(self, textvariable=self.var)
      entry.pack(fill='x', padx=24)
      entry.focus_set()
      bar = ctk.CTkFrame(self, fg_color='transparent')
      bar.pack(fill='x', padx=24, pady=22)
      ctk.CTkButton(bar, text='Cancel', fg_color='#555', command=self.destroy).pack(side='right', padx=(8, 0))
      ctk.CTkButton(bar, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(side='right')
      self.bind('<Return>', lambda _: _close_then(self, lambda: callback(self.var.get())))

class TextInputDialog(ctk.CTkToplevel):
  """Represent the TextInputDialog component and own its lifecycle within this module."""

  def __init__(self, master, title, label, callback, initial=''):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  title: Input used by the init operation.
  label: Input used by the init operation.
  callback: Input used by the init operation.
  initial: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title(title)
      self.geometry('460x210')
      self.transient(master)
      self.grab_set()
      self.var = ctk.StringVar(value=initial)
      ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text=label).pack(padx=24, anchor='w')
      e = ctk.CTkEntry(self, textvariable=self.var)
      e.pack(fill='x', padx=24, pady=8)
      e.focus_set()
      bar = ctk.CTkFrame(self, fg_color='transparent')
      bar.pack(fill='x', padx=24, pady=18)
      ctk.CTkButton(bar, text='Cancel', fg_color='#555', command=self.destroy).pack(side='right', padx=(8, 0))
      ctk.CTkButton(bar, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(side='right')

class ConfirmDialog(ctk.CTkToplevel):
  """Represent the ConfirmDialog component and own its lifecycle within this module."""

  def __init__(self, master, title, message, callback, confirm_text='Delete', confirm_color='#b33a3a'):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  title: Input used by the init operation.
  message: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title(title)
      self.geometry('500x210')
      self.transient(master)
      self.grab_set()
      ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text=message, wraplength=450, justify='left').pack(padx=24, anchor='w')
      bar = ctk.CTkFrame(self, fg_color='transparent')
      bar.pack(fill='x', padx=24, pady=25)
      ctk.CTkButton(bar, text='Cancel', fg_color='#555', command=self.destroy).pack(side='right', padx=(8, 0))
      ctk.CTkButton(bar, text=confirm_text, fg_color=confirm_color, command=lambda: _close_then(self, callback)).pack(side='right')

class PackageSelectionDialog(ctk.CTkToplevel):
  """Represent the PackageSelectionDialog component and own its lifecycle within this module."""

  def __init__(self, master, packages, callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  packages: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title('Add to Island Package')
      self.geometry('480x220')
      self.transient(master)
      self.grab_set()
      packages = sorted(packages, key=str.casefold)
      self.var = ctk.StringVar(value=packages[0])
      ctk.CTkLabel(self, text='Add to Island Package', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text='Island Package').pack(padx=24, anchor='w')
      ctk.CTkOptionMenu(self, values=packages, variable=self.var).pack(fill='x', padx=24, pady=8)
      ctk.CTkButton(self, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(padx=24, pady=20, anchor='e')

class YesNoDialog(ctk.CTkToplevel):
  """Represent the YesNoDialog component and own its lifecycle within this module."""

  def __init__(self, master, title, message, yes_callback, no_callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  title: Input used by the init operation.
  message: Input used by the init operation.
  yes_callback: Input used by the init operation.
  no_callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title(title)
      self.geometry('520x220')
      self.transient(master)
      self.grab_set()
      ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text=message, wraplength=470, justify='left').pack(padx=24, anchor='w')
      bar = ctk.CTkFrame(self, fg_color='transparent')
      bar.pack(fill='x', padx=24, pady=25)
      ctk.CTkButton(bar, text='No', fg_color='#555', command=lambda: _close_then(self, no_callback)).pack(side='right', padx=(8, 0))
      ctk.CTkButton(bar, text='Yes', command=lambda: _close_then(self, yes_callback)).pack(side='right')

class GuidDialog(ctk.CTkToplevel):
  """Represent the GuidDialog component and own its lifecycle within this module."""

  def __init__(self, master, current_guid, callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  current_guid: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title('Change GUID')
      self.geometry('450x210')
      self.transient(master)
      self.grab_set()
      self.var = ctk.StringVar(value=str(current_guid))
      validator = (self.register(lambda value: value == '' or value.isdigit()), '%P')
      ctk.CTkLabel(self, text='Change GUID', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text='New GUID').pack(padx=24, anchor='w')
      entry = ctk.CTkEntry(self, textvariable=self.var, validate='key', validatecommand=validator)
      entry.pack(fill='x', padx=24, pady=8)
      entry.focus_set()
      bar = ctk.CTkFrame(self, fg_color='transparent')
      bar.pack(fill='x', padx=24, pady=18)
      ctk.CTkButton(bar, text='Cancel', fg_color='#555', command=self.destroy).pack(side='right', padx=(8, 0))
      ctk.CTkButton(bar, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(side='right')

class RegionSelectionDialog(ctk.CTkToplevel):
  """Represent the RegionSelectionDialog component and own its lifecycle within this module."""

  def __init__(self, master, fixed_regions, custom_regions, current, callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  fixed_regions: Input used by the init operation.
  custom_regions: Input used by the init operation.
  current: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title('Set Region')
      self.geometry('470x240')
      self.transient(master)
      self.grab_set()
      fixed = sorted(fixed_regions, key=str.casefold)
      custom = sorted(custom_regions, key=str.casefold)
      values = fixed + (['──────── Custom Regions ────────'] if custom else []) + custom
      initial = current if current in values else fixed[0] if fixed else custom[0] if custom else ''
      self.var = ctk.StringVar(value=initial)
      ctk.CTkLabel(self, text='Region', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      menu = ctk.CTkOptionMenu(self, values=values or [''], variable=self.var, command=lambda value: self.var.set(initial) if value.startswith('─') else None)
      menu.pack(fill='x', padx=24, pady=8)
      ctk.CTkButton(self, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(padx=24, pady=20, anchor='e')

class TypeSelectionDialog(ctk.CTkToplevel):
  """Represent the TypeSelectionDialog component and own its lifecycle within this module."""

  def __init__(self, master, current, callback):
      """Perform the init operation for this module responsibility.

Args:
  master: Input used by the init operation.
  current: Input used by the init operation.
  callback: Input used by the init operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
      super().__init__(master)
      self.title('Change Type')
      self.geometry('450x210')
      self.transient(master)
      self.grab_set()
      self.var = ctk.StringVar(value=current if current in ('Normal', 'Decoration', 'Starter') else 'Normal')
      ctk.CTkLabel(self, text='Change Type', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
      ctk.CTkLabel(self, text='Type').pack(padx=24, anchor='w')
      ctk.CTkOptionMenu(self, values=['Decoration', 'Normal', 'Starter'], variable=self.var).pack(fill='x', padx=24, pady=8)
      ctk.CTkButton(self, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(padx=24, pady=20, anchor='e')

class IslandSizeSelectionDialog(ctk.CTkToplevel):
    """Select the Anno 117 placeholder size stored for one or more islands."""
    def __init__(self, master, current, callback):
        super().__init__(master)
        self.title('Change Island Size')
        self.geometry('450x210')
        self.transient(master)
        self.grab_set()
        values = ['Auto', 'Medium', 'Large', 'XL']
        self.var = ctk.StringVar(value=current if current in values else 'Auto')
        ctk.CTkLabel(self, text='Change Island Size', font=ctk.CTkFont(size=20, weight='bold')).pack(padx=24, pady=(24, 10), anchor='w')
        ctk.CTkLabel(self, text='Island Size').pack(padx=24, anchor='w')
        ctk.CTkOptionMenu(self, values=values, variable=self.var).pack(fill='x', padx=24, pady=8)
        ctk.CTkButton(self, text='Apply', command=lambda: _close_then(self, lambda: callback(self.var.get()))).pack(padx=24, pady=20, anchor='e')
