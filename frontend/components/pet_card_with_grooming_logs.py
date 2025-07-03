from frontend.components.pet_card import PetCard
import customtkinter as ctk
from frontend.style.style import (
    create_label, 
    create_frame, 
    get_subtitle_font, 
    get_card_detail_font,
    get_card_title_font,
    get_card_icon_font
)
# FIX: Correct import for GroomingLogsController
from backend.controllers.grooming_controller import GroomingLogsController

class PetCardWithGroomingLogs(PetCard):
    def __init__(self, master, pet, image_store, owner=None, on_click=None, *args, **kwargs):
        # FIX: Use GroomingLogsController and correct method to get logs
        self.grooming_logs = GroomingLogsController().get_grooming_logs_for_pet(pet.id)
        super().__init__(master, pet, image_store, owner, on_click, *args, **kwargs)

    def _get_pet_thumbnail(self):
        try:
            if not self.pet.image_path:
                raise FileNotFoundError
            import os
            from PIL import Image
            img_path = os.path.join("backend", "data", self.pet.image_path)
            if not os.path.exists(img_path):
                raise FileNotFoundError
            from customtkinter import CTkImage
            image = Image.open(img_path).resize((140, 140))
            thumb = CTkImage(light_image=image, dark_image=image, size=(140, 140))
            self.image_store.append(thumb)
            return thumb
        except Exception:
            from PIL import Image
            from customtkinter import CTkImage
            image = Image.new("RGB", (140, 140), color="lightgray")
            thumb = CTkImage(light_image=image, dark_image=image, size=(140, 140))
            self.image_store.append(thumb)
            self._missing_image = True
            return thumb

    def _build_card(self):
        # Main container
        container = create_frame(self, "white")
        container.pack(padx=12, pady=12, fill="both", expand=True)

        # Horizontal layout: left (details), right (image)
        main_row = create_frame(container, "white")
        main_row.pack(fill="both", expand=True)

        # --- LEFT: Info Section ---
        info_frame = create_frame(main_row, "white")
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Name with icon
        name_frame = create_frame(info_frame, "white")
        name_frame.pack(pady=(0, 8), anchor="w")
        ctk.CTkLabel(
            name_frame,
            text="🐾",
            font=get_card_icon_font(),
        ).pack(side="left", padx=(0, 5))
        label_name = create_label(
            name_frame,
            self.pet.name,
            font=get_card_title_font()
        )
        label_name.pack(side="left")

        # Details with icon-text pairs
        details_frame = create_frame(info_frame, "white")
        details_frame.pack(fill="x", padx=8)

        # Breed row
        breed_row = create_frame(details_frame, "white")
        breed_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            breed_row,
            text="🐶",
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            breed_row,
            self.pet.breed or "Unknown",
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Birthdate row
        birth_row = create_frame(details_frame, "white")
        birth_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            birth_row,
            text="📅",
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            birth_row,
            self.pet.birthdate,
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Age row
        age_row = create_frame(details_frame, "white")
        age_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            age_row,
            text="🕒",
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            age_row,
            self.pet.age(),
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Owner row (only if owner exists)
        if self.owner:
            owner_row = create_frame(details_frame, "white")
            owner_row.pack(fill="x", pady=3)
            ctk.CTkLabel(
                owner_row,
                text="👤",
                font=get_card_icon_font(),
                width=24,
                anchor="w"
            ).pack(side="left")
            create_label(
                owner_row,
                f"{self.owner.name} ({self.owner.contact_number})",
                font=get_card_detail_font(),
                anchor="w"
            ).pack(side="left", padx=5)

        # --- RIGHT: Image Section ---
        image_frame = create_frame(main_row, "white")
        image_frame.pack(side="right", fill="y", padx=(10, 0))
        thumbnail = self._get_pet_thumbnail()
        label_image = ctk.CTkLabel(
            image_frame,
            image=thumbnail,
            text="",
            compound="top"
        )
        label_image.pack(anchor="center", pady=5)
        # Show message if image is missing
        if hasattr(self, '_missing_image') and self._missing_image:
            ctk.CTkLabel(
                image_frame,
                text="Oh no! I can't see your pet's cuteness",
                font=get_card_detail_font(),
                text_color="#888888"
            ).pack(pady=(8, 0))

        # --- BELOW: Grooming Logs Section ---
        logs_frame = create_frame(container, "white")
        logs_frame.pack(fill="x", pady=(10, 0))

        logs_label = create_label(logs_frame, "Grooming Logs:", font=get_subtitle_font())
        logs_label.pack(anchor="w")
        if self.grooming_logs:
            for log in self.grooming_logs:
                create_label(
                    logs_frame,
                    f"• {log}",
                    font=get_card_detail_font(),
                    anchor="w"
                ).pack(anchor="w", padx=10)
        else:
            create_label(
                logs_frame,
                "No grooming logs.",
                font=get_card_detail_font(),
                anchor="w"
            ).pack(anchor="w", padx=10)