import customtkinter as ctk
from frontend.style.style import create_label, create_frame, create_back_button, get_title_font, apply_uniform_layout_style, create_styled_back_button
from frontend.components.pet_card_with_records import PetCardWithRecords
from backend.controllers.pet_controller import PetController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.vet_visit_controller import VetVisitController
from backend.database_handlers.vaccinations_db_handler import VaccinationDB
from backend.database_handlers.vet_visits_db_handler import VetVisitDB

class VaccinationVisitsTab:
    @staticmethod
    def filter_pets_with_records(pet_list, vaccination_records, vet_visit_records):
        pet_ids = {rec.pet_id for rec in vaccination_records} | {rec.pet_id for rec in vet_visit_records}
        return [pet for pet in pet_list if pet.id in pet_ids]

    @classmethod
    def create(cls, parent, show_frame):
        # Clear existing widgets
        [w.destroy() for w in parent.winfo_children()]

        # Apply the uniform layout style (reuse main_frame logic from view_pets_tab)
        main_frame = apply_uniform_layout_style(parent)

        # Create the title label with the new styling
        create_label(main_frame, "💉 Vaccinations & Vet Visits", font=get_title_font()).pack(pady=(20, 15))

        # Create a frame for the canvas and scrollbar
        canvas_frame = create_frame(main_frame, fg_color="#f5f5f5")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the canvas and scrollable frame
        canvas = ctk.CTkCanvas(canvas_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(canvas_frame, command=canvas.yview)
        scrollable_frame = create_frame(canvas, fg_color="#f5f5f5")
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Configure the grid for the scrollable frame (3 columns for cards)
        for i in range(3):
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

        # Fetch data here
        pet_ctrl = PetController()
        vacc_ctrl = VaccinationController()
        vet_ctrl = VetVisitController()
        pets, owners = pet_ctrl.get_pets_with_owners()
        vacc_db = VaccinationDB()
        vet_db = VetVisitDB()
        vaccinations = vacc_db.get_all()
        vet_visits = vet_db.get_all()
        image_store = []  # Or fetch as needed
        owner_lookup = {owner.id: owner for owner in owners if owner}

        pets_with_records = cls.filter_pets_with_records(pets, vaccinations, vet_visits)

        if not pets_with_records:
            create_label(scrollable_frame, "No pets with vaccination or vet visit records.").pack(pady=40)
        else:
            for idx, pet in enumerate(pets_with_records):
                owner = owner_lookup.get(pet.owner_id)
                vet_visits = vet_ctrl.get_by_pet_id(pet.id)
                vaccinations = vacc_ctrl.get_by_pet_id(pet.id)
                from backend.controllers.feeding_log_controller import FeedingLogController
                from backend.controllers.grooming_controller import GroomingLogsController
                feeding_logs = FeedingLogController().get_by_pet_id(pet.id)
                grooming_logs = GroomingLogsController().get_grooming_logs_for_pet(pet.id)
                card = PetCardWithRecords(
                    scrollable_frame, pet, image_store, owner=owner,
                    on_click=lambda pet=pet, owner=owner, vet_visits=vet_visits, vaccinations=vaccinations, feeding_logs=feeding_logs, grooming_logs=grooming_logs:
                        show_frame(
                            "pet_profile",
                            pet=pet,
                            owner=owner,
                            vet_visits=vet_visits,
                            vaccinations=vaccinations,
                            feeding_logs=feeding_logs,
                            grooming_logs=grooming_logs
                        )
                )
                row, col = divmod(idx, 3)
                card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
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

        return parent