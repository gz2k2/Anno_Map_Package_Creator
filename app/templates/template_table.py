"""Reusable dark-mode sortable table component. It centralizes Treeview styling, column sizing, row replacement, and numeric/text sorting for application tables."""
import customtkinter as ctk
from tkinter import ttk
from tkinter import font as tkfont

class SortableTable(ctk.CTkFrame):
    """Represent the SortableTable component and own its lifecycle within this module."""

    def __init__(self, master, columns, **kw):
        """Perform the init operation for this module responsibility.

Args:
    master: Input used by the init operation.
    columns: Input used by the init operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        super().__init__(master, fg_color='#242424', **kw)
        style = ttk.Style(self)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        name = f'Dark{id(self)}.Treeview'
        style.configure(name, background='#242424', fieldbackground='#242424', foreground='#f2f2f2', rowheight=30, borderwidth=0)
        style.map(name, background=[('selected', '#1f6aa5')], foreground=[('selected', '#fff')])
        style.configure(name + '.Heading', background='#2b2b2b', foreground='#f2f2f2', relief='flat', padding=(8, 7), font=('Segoe UI', 10, 'bold'))
        style.map(name + '.Heading', background=[('active', '#3a3a3a')])
        self.tree = ttk.Treeview(self, columns=[c[0] for c in columns], show='headings', style=name, selectmode='extended')
        for k, h, width in columns:
            self.tree.heading(k, text=f'{h} ↕', command=lambda x=k: self.sort_by(x, False))
            self.tree.column(k, width=width, minwidth=70, anchor='w')
        vscroll = ctk.CTkScrollbar(self, command=self.tree.yview)
        hscroll = ctk.CTkScrollbar(self, orientation='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vscroll.grid(row=0, column=1, sticky='ns', padx=(4, 0))
        hscroll.grid(row=1, column=0, sticky='ew', pady=(4, 0))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def set_rows(self, rows):
        """Perform the set rows operation for this module responsibility.

Args:
    rows: Input used by the set rows operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', 'end', values=row)
        self._autosize_columns(rows)

    def _autosize_columns(self, rows):
        """Perform the autosize columns operation for this module responsibility.

Args:
    rows: Input used by the autosize columns operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        font = tkfont.nametofont('TkDefaultFont')
        heading_font = tkfont.Font(family='Segoe UI', size=10, weight='bold')
        for index, column in enumerate(self.tree['columns']):
            heading = self.tree.heading(column, 'text')
            width = heading_font.measure(heading) + 28
            for row in rows:
                if index < len(row):
                    width = max(width, font.measure(str(row[index])) + 28)
            self.tree.column(column, width=width, minwidth=70, stretch=False)

    def sort_by(self, col, rev):
        """Perform the sort by operation for this module responsibility.

Args:
    col: Input used by the sort by operation.
    rev: Input used by the sort by operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""

        def key(i):
            """Perform the key operation for this module responsibility.

Args:
    i: Input used by the key operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
            v = self.tree.set(i, col)
            try:
                return (0, int(v))
            except ValueError:
                return (1, v.casefold())
        for n, i in enumerate(sorted(self.tree.get_children(), key=key, reverse=rev)):
            self.tree.move(i, '', n)
        for c in self.tree['columns']:
            text = self.tree.heading(c, 'text').replace(' ▲', '').replace(' ▼', '').replace(' ↕', '')
            self.tree.heading(c, text=text + ((' ▼' if rev else ' ▲') if c == col else ' ↕'))
        self.tree.heading(col, command=lambda: self.sort_by(col, not rev))
