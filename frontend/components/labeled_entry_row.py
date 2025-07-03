import customtkinter as ctk

class LabeledEntryRow(ctk.CTkFrame):
    def __init__(self, parent, label, entry_widget, **kwargs):
        super().__init__(parent, fg_color="transparent")
        self.label = ctk.CTkLabel(self, text=label, font=kwargs.get("font"))
        self.label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.entry = entry_widget
        self.entry.grid(row=0, column=1, sticky="ew")
        self.grid_columnconfigure(1, weight=1)