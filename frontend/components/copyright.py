import datetime
import customtkinter as ctk  # Or use tkinter if you're not on CTk

def get_copyright_label(master):
    current_year = datetime.datetime.now().year
    copyright_str = f"© {current_year} G. Eman, S. D. Calzada, S. Pula, U.R. Orillia. All rights reserved."
    return ctk.CTkLabel(master=master, text=copyright_str,
                        font=ctk.CTkFont(size=10, weight="normal"),
                        text_color="gray")