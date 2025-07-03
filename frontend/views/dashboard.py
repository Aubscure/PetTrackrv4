import customtkinter as ctk

from frontend.style.style import (
    create_label,
    create_frame,
    create_exit_button,
)
from frontend.components.dashboard_buttons import (
    add_pet_button,
    view_pets_button,
    vaccinations_button,
    grooming_button,
    daycare_button,
)

def create_dashboard(parent, show_frame):
    for widget in parent.winfo_children():
        widget.destroy()

    # Title
    title = create_label(parent, "🐾 PetTrackr Dashboard")
    title.pack(pady=(20, 10))

    # Main container for bento grid (centered and compact)
    main_frame = create_frame(parent)
    main_frame.pack(expand=True)
    main_frame.configure(width=600, height=400)
    main_frame.pack_propagate(False)

    # Bento grid container (centered)
    grid_frame = create_frame(main_frame)
    grid_frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- Row 1: Large Add Pet, two stacked small buttons ---
    row1 = create_frame(grid_frame)
    row1.pack()

    add_pet_btn = add_pet_button(row1, show_frame)
    add_pet_btn.configure(width=320, height=200)
    add_pet_btn.pack(side="left", padx=(0, 8))

    right_col = create_frame(row1)
    right_col.pack(side="left")

    view_pets_btn = view_pets_button(right_col, show_frame)
    view_pets_btn.configure(width=140, height=95)
    view_pets_btn.pack(pady=(0, 8))

    vaccinations_btn = vaccinations_button(right_col, show_frame)
    vaccinations_btn.configure(width=140, height=95)
    vaccinations_btn.pack(pady=(8, 0))

    # --- Row 2: Groomings, Daycare, Exit (all medium) ---
    row2 = create_frame(grid_frame)
    row2.pack(pady=(8, 0))

    grooming_btn = grooming_button(row2, show_frame)
    grooming_btn.configure(width=120, height=80)
    grooming_btn.pack(side="left", padx=(0, 8))

    daycare_btn = daycare_button(row2, show_frame)
    daycare_btn.configure(width=120, height=80)
    daycare_btn.pack(side="left", padx=(0, 8))

    exit_btn = create_exit_button(
        row2,
        text="Exit",
        command=parent.quit,
        width=120,
        height=80
    )
    exit_btn.pack(side="left")

    return parent