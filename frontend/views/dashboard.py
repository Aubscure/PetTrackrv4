import customtkinter as ctk
from frontend.components.copyright import get_copyright_label

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

def create_vaccination_visits_button(parent, show_frame):
    # Combines vaccination and visits (assuming visits = vet visits)
    return vaccinations_button(parent, show_frame)  # You can update text/icon if needed


def create_dashboard(parent, show_frame):
    for widget in parent.winfo_children():
        widget.destroy()

    # Title (centered at the top)
    title = create_label(parent, "🐾 PetTrackr Dashboard")
    title.pack(side="top", pady=(40, 20), anchor="n", fill="x")
    title.configure(justify="center")

    # Main container for bento grid (centered, 3/4 of the screen)
    main_frame = create_frame(parent)
    main_frame.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.75, relheight=0.75)
    main_frame.pack_propagate(False)

    # Bento grid container (fills main_frame)
    grid_frame = create_frame(main_frame)
    grid_frame.pack(expand=True, fill="both", padx=20, pady=10)
    grid_frame.grid_propagate(False)
    grid_frame.configure(width=560, height=420)

    # Configure grid weights for stretching
    for i in range(4):
        grid_frame.rowconfigure(i, weight=1, uniform="row")
    for j in range(2):
        grid_frame.columnconfigure(j, weight=1, uniform="col")

    # 1. Add Pet (most important, large, spans two columns)
    add_pet_btn = add_pet_button(grid_frame, show_frame)
    add_pet_btn.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=8, pady=8)
    add_pet_btn.configure(width=1, height=1)  # Let grid stretch

    # 2. View All Pets
    view_pets_btn = view_pets_button(grid_frame, show_frame)
    view_pets_btn.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
    view_pets_btn.configure(width=1, height=1)

    # 3. Vaccination & Visits (combined)
    vacc_visits_btn = create_vaccination_visits_button(grid_frame, show_frame)
    vacc_visits_btn.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)
    vacc_visits_btn.configure(width=1, height=1)

    # 4. Daycare
    daycare_btn = daycare_button(grid_frame, show_frame)
    daycare_btn.grid(row=2, column=0, sticky="nsew", padx=8, pady=8)
    daycare_btn.configure(width=1, height=1)

    # 5. Grooming
    grooming_btn = grooming_button(grid_frame, show_frame)
    grooming_btn.grid(row=2, column=1, sticky="nsew", padx=8, pady=8)
    grooming_btn.configure(width=1, height=1)

    # 6. Exit (spans two columns, smaller)
    exit_btn = create_exit_button(
        grid_frame,
        text="Exit",
        command=parent.quit,
        width=1,
        height=1
    )
    exit_btn.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=8, pady=(8, 0))

    copyright_label = get_copyright_label(main_frame)
    copyright_label.pack(side="bottom", pady=(2, 2))

    return parent