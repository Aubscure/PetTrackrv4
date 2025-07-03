#frontend/views/view_pets_tab.py
import customtkinter as ctk
from backend.models import owner
from frontend.components.pet_card import PetCard
from backend.controllers.pet_controller import PetController
from frontend.style.style import create_label, create_button, create_frame, get_title_font, apply_uniform_layout_style, create_styled_back_button
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController
from frontend.components.copyright import get_copyright_label

def get_vet_visits(pet_id): return VetVisitController().get_by_pet_id(pet_id)
def get_vaccinations(pet_id): return VaccinationController().get_by_pet_id(pet_id)
def get_feeding_logs(pet_id): return FeedingLogController().get_by_pet_id(pet_id)

def create_view_pets_tab(parent, show_frame):
    # Clear existing widgets
    [w.destroy() for w in parent.winfo_children()]

    # Apply the uniform layout style
    main_frame = apply_uniform_layout_style(parent)

    # Create the title label with the new styling
    create_label(main_frame, "📋 All Pets", font=get_title_font()).pack(pady=(20, 15))

    # Create a frame for the canvas and scrollbar
    canvas_frame = create_frame(main_frame, fg_color="#F0F8FF")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create the canvas and scrollable frame
    canvas = ctk.CTkCanvas(canvas_frame, bg="#F0F8FF", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(canvas_frame, command=canvas.yview)
    scrollable_frame = create_frame(canvas, fg_color="#F0F8FF")
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Configure the grid for the scrollable frame
    for i in range(4):
        scrollable_frame.columnconfigure(i, weight=1, uniform="column", minsize=260)

    # Bind events for scrolling
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_linux_scroll(event):
        if event.num in (4, 5):
            canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    for seq, func in [("<MouseWheel>", _on_mousewheel), ("<Button-4>", _on_linux_scroll), ("<Button-5>", _on_linux_scroll)]:
        canvas.bind_all(seq, func)

    canvas.bind("<Configure>", on_canvas_configure)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=(0, 4))
    scrollbar.pack(side="right", fill="y", padx=(0, 8))

    # Create and place the pet cards
    thumbnails = []
    pets, owners = PetController().get_pets_with_owners()
    for i, (pet, owner_obj) in enumerate(zip(pets, owners)):
        row, col = divmod(i, 4)
        PetCard(
            scrollable_frame,
            pet,
            thumbnails,
            owner=owner_obj,
            on_click=lambda pet=pet, owner=owner_obj: show_frame(
                "pet_profile",
                pet=pet,
                owner=owner,
                vet_visits=get_vet_visits(pet.id),
                vaccinations=get_vaccinations(pet.id),
                feeding_logs=get_feeding_logs(pet.id)
            )
        ).grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        scrollable_frame.rowconfigure(row, weight=1)

    # Create a styled back button
    btn_wrapper = create_frame(main_frame, fg_color="transparent")
    btn_wrapper.pack(pady=20)
    create_styled_back_button(
        btn_wrapper,
        text="⬅️ Back to Dashboard",
        command=lambda: show_frame("dashboard"),
        width=220
    ).pack()

    def cleanup():
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            canvas.unbind_all(seq)

    parent.bind("<Destroy>", lambda e: cleanup())

    copyright_label = get_copyright_label(main_frame)
    copyright_label.pack(side="bottom", pady=(2, 2))

    return parent
