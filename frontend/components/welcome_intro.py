import customtkinter as ctk
from frontend.style.style import get_title_font, get_subtitle_font, get_entry_font

def create_welcome_intro(parent):
    """Creates a welcome introduction section with balanced design"""
    
    # Main welcome frame with subtle background
    welcome_frame = ctk.CTkFrame(
        parent, 
        fg_color="#F8FAFC", 
        corner_radius=12,
        border_width=1,
        border_color="#E2E8F0"
    )
    
    # Inner content frame
    content_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
    content_frame.pack(expand=True, fill="both", padx=24, pady=20)
    
    # Title with paw emoji
    title = ctk.CTkLabel(
        content_frame,
        text="🐾 Welcome to PetTrackr",
        font=get_title_font(size=26),
        text_color="#1A202C"
    )
    title.pack(pady=(0, 8))
    
    # Subtitle
    subtitle = ctk.CTkLabel(
        content_frame,
        text="Your all-in-one solution for smarter pet care!",
        font=get_subtitle_font(),
        text_color="#4A5568"
    )
    subtitle.pack(pady=(0, 20))
    
    # Description text with better formatting
    description_text = (
        "PetTrackr is a desktop app built for pet care teams. It lets you organize pet profiles, "
        "health records, feeding schedules, grooming logs, and vet visits—all in one place. "
        "With a clear and easy-to-use interface, staff can track important details, stay on schedule, "
        "and give pets the care they deserve."
    )
    
    description = ctk.CTkLabel(
        content_frame,
        text=description_text,
        font=ctk.CTkFont(family="Segoe UI", size=14),
        text_color="#4A5568",
        justify="left",
        wraplength=700  # Increased wrap length for better layout
    )
    description.pack(pady=(0, 0))
    
    return welcome_frame 