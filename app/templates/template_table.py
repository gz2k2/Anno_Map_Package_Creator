"""Reusable sortable ttk Treeview table hosted in a CustomTkinter frame."""
import customtkinter as ctk
from tkinter import ttk

class SortableTable(ctk.CTkFrame):
    """Provide configurable columns, selection, scrolling, and typed sorting."""
    def __init__(self, master, columns: list[tuple[str, str, int]], **kwargs):
        super().__init__(master, **kwargs)
        self._columns = columns
        self.tree = ttk.Treeview(self, columns=[c[0] for c in columns], show="headings")
        for key, heading, width in columns:
            self.tree.heading(key, text=heading, command=lambda k=key: self.sort_by(k, False))
            self.tree.column(key, width=width, minwidth=70, anchor="w")
        scroll = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(0, weight=1)

    def set_rows(self, rows: list[tuple]) -> None:
        """Replace all visible rows with the supplied values."""
        self.tree.delete(*self.tree.get_children())
        for row in rows: self.tree.insert("", "end", values=row)

    def sort_by(self, column: str, reverse: bool) -> None:
        """Sort a column numerically when possible and otherwise as text."""
        def key(item):
            value = self.tree.set(item, column)
            try: return (0, int(value))
            except ValueError: return (1, value.casefold())
        items = sorted(self.tree.get_children(""), key=key, reverse=reverse)
        for index, item in enumerate(items): self.tree.move(item, "", index)
        self.tree.heading(column, command=lambda: self.sort_by(column, not reverse))
