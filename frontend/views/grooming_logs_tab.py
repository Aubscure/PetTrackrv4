import customtkinter as ctk
from backend.controllers.pet_controller import PetController
from frontend.components.pet_card_with_grooming_logs import PetCardWithGroomingLogs
from frontend.style.style import create_label, create_frame, create_back_button

def create_grooming_logs_tab(master, show_frame):
    # Clear the master frame
    for widget in master.winfo_children():
        widget.destroy()

    # Configure master grid
    master.grid_rowconfigure(0, weight=1)  # For main container
    master.grid_rowconfigure(1, weight=0)  # For bottom frame
    master.grid_columnconfigure(0, weight=1)

    # Create main container frame
    main_container = ctk.CTkFrame(master)
    main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 0))
    
    # Configure main container grid
    main_container.grid_rowconfigure(0, weight=0)  # Title
    main_container.grid_rowconfigure(1, weight=1)  # Content
    main_container.grid_columnconfigure(0, weight=1)

    # Title label at the top
    title_label = create_label(main_container, "🛁 Grooming Logs")
    title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")

    # Content frame that will hold the cards
    content_frame = create_frame(main_container)
    content_frame.grid(row=1, column=0, sticky="nsew")
    
    # Configure content frame grid
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # Cards frame for pet cards
    try:
        cards_frame = ctk.CTkScrollableFrame(content_frame)
    except AttributeError:
        import tkinter as tk
        canvas = tk.Canvas(content_frame)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
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
        cards_frame.grid(row=0, column=0, sticky="nsew")
    cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

    pet_controller = PetController()
    pets, owners = pet_controller.get_pets_with_owners()
    image_store = []

    # Only show pets with grooming logs
    from backend.controllers.grooming_controller import GroomingLogsController
    from backend.controllers.feeding_log_controller import FeedingLogController
    from backend.controllers.vaccination_controller import VaccinationController
    from backend.controllers.vet_visit_controller import VetVisitController

    grooming_ctrl = GroomingLogsController()
    feeding_ctrl = FeedingLogController()
    vacc_ctrl = VaccinationController()
    vet_ctrl = VetVisitController()

    pets_with_logs = []
    owners_with_logs = []
    for pet, owner in zip(pets, owners):
        logs = grooming_ctrl.get_grooming_logs_for_pet(pet.id)
        if logs:
            pets_with_logs.append(pet)
            owners_with_logs.append(owner)

    if not pets_with_logs:
        no_pets_label = create_label(cards_frame, "No pets with grooming logs found.")
        no_pets_label.grid(row=0, column=0, pady=40)
    else:
        for idx, (pet, owner) in enumerate(zip(pets_with_logs, owners_with_logs)):
            vet_visits = vet_ctrl.get_by_pet_id(pet.id)
            vaccinations = vacc_ctrl.get_by_pet_id(pet.id)
            feeding_logs = feeding_ctrl.get_by_pet_id(pet.id)
            grooming_logs = grooming_ctrl.get_grooming_logs_for_pet(pet.id)
            def on_card_click(
                pet=pet, owner=owner, vet_visits=vet_visits, vaccinations=vaccinations,
                feeding_logs=feeding_logs, grooming_logs=grooming_logs
            ):
                show_frame(
                    "pet_profile",
                    pet=pet,
                    owner=owner,
                    vet_visits=vet_visits,
                    vaccinations=vaccinations,
                    feeding_logs=feeding_logs,
                    grooming_logs=grooming_logs
                )
            card = PetCardWithGroomingLogs(
                cards_frame, pet, image_store, owner=owner, on_click=on_card_click
            )
            row, col = divmod(idx, 3)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

    # Bottom frame for the back button (outside main container)
    bottom_frame = ctk.CTkFrame(master)
    bottom_frame.grid(row=1, column=0, sticky="se", padx=20, pady=(0, 20))
    bottom_frame.grid_columnconfigure(0, weight=1)

    # Back button aligned to the right
    back_button = ctk.CTkButton(
        bottom_frame,
        text="Back",
        command=lambda: show_frame("dashboard"),
        width=120
    )
    back_button.grid(row=0, column=0, sticky="e", padx=0, pady=0)

    return master