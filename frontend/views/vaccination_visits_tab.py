import customtkinter as ctk
from frontend.style.style import create_label, create_frame, create_back_button
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
        for widget in parent.winfo_children():
            widget.destroy()

        create_label(parent, "💉 Vaccinations & Vet Visits").pack(pady=(20, 10))

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

        main_frame = create_frame(parent)
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Add scrollable frame for cards
        try:
            cards_frame = ctk.CTkScrollableFrame(main_frame)
        except AttributeError:
            # Fallback for older customtkinter: use canvas+frame+scrollbar
            import tkinter as tk
            canvas = tk.Canvas(main_frame)
            scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            cards_frame = create_frame(canvas)
            cards_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=cards_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            cards_frame.pack(expand=True, fill="both")
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        if not pets_with_records:
            create_label(cards_frame, "No pets with vaccination or vet visit records.").pack(pady=40)
        else:
            for idx, pet in enumerate(pets_with_records):
                owner = owner_lookup(pet.owner_id) if callable(owner_lookup) else owner_lookup.get(pet.owner_id)
                vet_visits = vet_ctrl.get_by_pet_id(pet.id)
                vaccinations = vacc_ctrl.get_by_pet_id(pet.id)
                # If you have a FeedingLogController and GroomingLogController, use them:
                from backend.controllers.feeding_log_controller import FeedingLogController
                from backend.controllers.grooming_controller import GroomingLogsController
                feeding_logs = FeedingLogController().get_by_pet_id(pet.id)
                grooming_logs = GroomingLogsController().get_grooming_logs_for_pet(pet.id)
                card = PetCardWithRecords(
                    cards_frame, pet, image_store, owner=owner,
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

        back_btn_frame = create_frame(parent)
        back_btn_frame.pack(side="bottom", anchor="se", pady=20, padx=20, fill="x")
        back_btn_frame.grid_columnconfigure(0, weight=1)
        create_back_button(
            back_btn_frame,
            text="Back",
            command=lambda: show_frame("dashboard"),
            width=120
        ).grid(row=0, column=1, sticky="e")

        return parent