import customtkinter as ctk
from frontend.style.style import get_button_font, PRIMARY_COLOR

class CTkModernButton(ctk.CTkFrame):
    def __init__(self, master, text="", command=None, width=200, color=PRIMARY_COLOR, **kwargs):
        super().__init__(master, fg_color="transparent")

        self.button = ctk.CTkButton(
            self,
            text=text,
            command=command,
            fg_color=color,
            corner_radius=8,
            font=get_button_font(),
            width=width,
            **kwargs
        )
        self.button.pack(fill="both", expand=True)

    def grid(self, **kwargs):
        return super().grid(**kwargs)

    def pack(self, **kwargs):
        return super().pack(**kwargs)

    def place(self, **kwargs):
        return super().place(**kwargs)

    def configure(self, **kwargs):
        self.button.configure(**kwargs)

    def set_text(self, text):
        self.button.configure(text=text)