import customtkinter as ctk
from frontend.components.copyright import get_copyright_label
from frontend.components.slideshow import Slideshow
from frontend.components.welcome_intro import create_welcome_intro
from frontend.style.style import (
    create_label,
    create_exit_button,
)
from frontend.components.dashboard_buttons import (
    add_pet_button,
    view_pets_button,
    vaccinations_button,
    grooming_button,
    daycare_button,
)

def create_vaccination_visits_button(parent, show_frame):
    # Combines vaccination and visits (assuming visits = vet visits)
    return vaccinations_button(parent, show_frame)  # You can update text/icon if needed


def create_dashboard(parent, show_frame):
    for widget in parent.winfo_children():
        widget.destroy()

    # Create a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Welcome introduction section
    welcome_section = create_welcome_intro(scrollable_frame)
    welcome_section.pack(side="top", pady=(0, 30), fill="x", padx=40)

    # Main content frame with 2 columns
    main_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    main_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
    
    # Configure grid weights for 2 columns
    main_frame.grid_columnconfigure(0, weight=1)  # Left column (slideshow)
    main_frame.grid_columnconfigure(1, weight=1)  # Right column (buttons)
    main_frame.grid_rowconfigure(0, weight=1)

    # Left column: Slideshow
    slideshow_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    slideshow_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    
    slideshow = Slideshow(slideshow_frame)
    slideshow.pack(expand=True, fill="both")

    # Right column: Buttons
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    # 1. Add Pet (large)
    add_pet_btn = add_pet_button(button_frame, show_frame)
    add_pet_btn.pack(fill="x", padx=8, pady=8)

    # 2. View All Pets & Vaccination/Visits (side by side)
    row1 = ctk.CTkFrame(button_frame, fg_color="transparent")
    row1.pack(fill="x", padx=8, pady=8)
    view_pets_btn = view_pets_button(row1, show_frame)
    view_pets_btn.pack(side="left", expand=True, fill="x", padx=(0,4))
    vacc_visits_btn = create_vaccination_visits_button(row1, show_frame)
    vacc_visits_btn.pack(side="left", expand=True, fill="x", padx=(4,0))

    # 3. Daycare & Grooming (side by side)
    row2 = ctk.CTkFrame(button_frame, fg_color="transparent")
    row2.pack(fill="x", padx=8, pady=8)
    daycare_btn = daycare_button(row2, show_frame)
    daycare_btn.pack(side="left", expand=True, fill="x", padx=(0,4))
    grooming_btn = grooming_button(row2, show_frame)
    grooming_btn.pack(side="left", expand=True, fill="x", padx=(4,0))

    # 4. Exit (full width)
    exit_btn = create_exit_button(
        button_frame,
        text="Exit",
        command=parent.quit,
        width=1,
        height=1
    )
    exit_btn.pack(fill="x", padx=8, pady=(8, 0))

    # Copyright at the bottom (outside scrollable frame)
    copyright_label = get_copyright_label(parent)
    copyright_label.pack(side="bottom", pady=(2, 2))

    return parent