import tkinter as tk
from tkinter import font
from customtkinter import CTkLabel
from frontend.style.style import (
    get_entry_font,
    get_placeholder_font,
    get_placeholder_color,
    get_placeholder_bg,
    PLACEHOLDER_OFFSET_Y,
    ENTRY_HEIGHT
)

class FloatingPlaceholderEntry(tk.Frame):
    def __init__(self, parent, placeholder: str, *args, **kwargs):
        super().__init__(parent)

        # Fonts for animation (adjust size as needed)
        self.normal_font = get_entry_font()
        self.small_font = get_placeholder_font()

        self.entry = tk.Entry(self, *args, **kwargs, font=self.normal_font)
        self.entry.pack(fill="both", padx=6, pady=10, ipady=ENTRY_HEIGHT // 3)

        self.placeholder_text = placeholder


        self.placeholder = CTkLabel(
            self,
            text=placeholder,
            font=self.normal_font,
            text_color=get_placeholder_color(),
            fg_color=get_placeholder_bg()
        )

        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyRelease>", self._on_key_release)

    def _float_placeholder(self):
        self.placeholder.configure(font=self.small_font)
        self.placeholder.place(relx=0, rely=0, anchor="nw", x=5, y=PLACEHOLDER_OFFSET_Y)

    def _restore_placeholder(self):
        if not self.entry.get():
            self.placeholder.configure(font=self.normal_font)
            self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def _on_focus_in(self, event):
        if not self.entry.get():
            self._float_placeholder()

    def _on_focus_out(self, event):
        self._restore_placeholder()

    def _on_key_release(self, event):
        if self.entry.get():
            self._float_placeholder()
        else:
            self._restore_placeholder()

    def get(self):
        return self.entry.get()

    def delete(self, start, end):
        self.entry.delete(start, end)

    def insert(self, index, text):
        self.entry.insert(index, text)