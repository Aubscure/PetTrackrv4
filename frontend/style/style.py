import customtkinter as ctk
from tkinter import ttk

# === Appearance ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# === Fonts ===
def get_title_font(size=28):
    return ctk.CTkFont(family="Segoe UI", size=size, weight="bold")

def get_button_font(size=20):
    return ctk.CTkFont(family="Segoe UI", size=size)

def get_subtitle_font():
    return ctk.CTkFont(family="Segoe UI", size=18)

def get_entry_font():
    return ctk.CTkFont(family="Segoe UI", size=16)

def get_placeholder_font():
    return ctk.CTkFont(family="Segoe UI", size=12)

def get_card_title_font():
    return ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

def get_card_detail_font():
    return ctk.CTkFont(family="Segoe UI", size=13)

def get_card_icon_font():
    return ctk.CTkFont(family="Segoe UI", size=12)

# === Colors ===
PRIMARY_COLOR = "#3b8ed0"
PRIMARY_HOVER_COLOR = "#6bb8f7"
SECONDARY_COLOR = "#8c8c8c"
DANGER_COLOR = "#ff5e5e"
DANGER_HOVER = "#ff3e3e"
TRANSPARENT = "transparent"

def get_placeholder_color():
    """Returns the placeholder text color"""
    return PLACEHOLDER_COLOR

def get_placeholder_bg():
    """Returns the placeholder background color"""
    return PLACEHOLDER_BG
        
        

# === Components ===
def create_button(master, text, command, color=PRIMARY_COLOR, width=200, **kwargs):
    return ctk.CTkButton(
        master,
        text=text,
        fg_color=color,
        hover_color=PRIMARY_HOVER_COLOR,
        corner_radius=8,
        font=get_button_font(),
        command=command,
        width=width,
        **kwargs
    )

def create_back_button(master, text, command, color=SECONDARY_COLOR, width=200, **kwargs):
    return ctk.CTkButton(
        master,
        text=text,
        fg_color=color,
        hover_color=DANGER_HOVER,
        corner_radius=8,
        font=get_button_font(),
        command=command,
        width=width,
        **kwargs
    )

def create_exit_button(master, text, command, color=DANGER_COLOR, width=200, **kwargs):
    return ctk.CTkButton(
        master,
        text=text,
        fg_color=color,
        hover_color=DANGER_HOVER,
        corner_radius=8,
        font=get_button_font(),
        command=command,
        width=width,
        **kwargs
    )
def create_label1(parent, text, font=None, **kwargs):
    return ctk.CTkLabel(parent, text=text, font=font, **kwargs)

def create_label(master, text, font=None, **kwargs):
    return ctk.CTkLabel(
        master,
        text=text,
        font=font or get_title_font(),
        text_color="#222222",
        **kwargs
    )

def create_frame(master, fg_color=TRANSPARENT):
    return ctk.CTkFrame(master, fg_color=fg_color)

def create_bento_button(parent, text, command, color="default", width=200, height=120):
    """Create a bento-style button with rounded corners and shadow"""
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=12,
        border_width=0,
        fg_color=("#F0F2F5", "#2A2D35") if color == "default" else color,
        hover_color=("#DCE0E5", "#373B45") if color == "default" else color,
        font=get_button_font(size=16),
        text_color=("#2A2D35", "#F0F2F5")
    )
    # Add shadow effect
    btn.configure(border_spacing=10)
    return btn


# === Card Components ===
def create_card_frame(master):
    return ctk.CTkFrame(master, fg_color="#e0e0e0", corner_radius=10)

def create_field_row(master):
    return ctk.CTkFrame(master, fg_color=TRANSPARENT)

# === Constants ===
PADDING_Y = 10
PADDING_X = 10
PLACEHOLDER_OFFSET_Y = -6  # Slightly taller float
ENTRY_HEIGHT = 44
PLACEHOLDER_COLOR = "#676767"
PLACEHOLDER_BG = "#ffffff"  # white background

# === Table Styles ===
def configure_table_style():
    style = ttk.Style()
    style.configure("Treeview", rowheight=32, font=("Segoe UI", 14))
    style.configure("Treeview.Heading", font=("Segoe UI", 16, "bold"))



# Add this function to your style.py module
def apply_uniform_layout_style(parent, bg_color="#F0F8FF"):
    # Set the background color of the parent widget
    parent.configure(fg_color=bg_color)

    # Create a main frame with padding to add depth
    main_frame = create_frame(parent, fg_color=bg_color)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    return main_frame

def create_styled_back_button(parent, text, command, width=220):
    """Create a styled back button with light brown color"""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        corner_radius=8,
        font=get_button_font(),
        fg_color="#b8a38a",  # Light brown color
        hover_color="#c9b69a",  # Slightly lighter brown for hover effect
        text_color="#222222"  # Dark text color for contrast
    )
