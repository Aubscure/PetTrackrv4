import customtkinter as ctk

class LabeledRadioGroup(ctk.CTkFrame):
    def __init__(self, parent, label, options, variable, **kwargs):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text=label, font=kwargs.get("font")).pack(anchor="w", pady=(0, 6))
        for text, value in options:
            ctk.CTkRadioButton(self, text=text, variable=variable, value=value).pack(anchor="w", padx=10, pady=2)