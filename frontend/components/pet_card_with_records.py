import os
import random
from PIL import Image
import customtkinter as ctk
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.vet_visit_controller import VetVisitController

def create_label(master, text, font, anchor="center", **kwargs):
    return ctk.CTkLabel(master, text=text, font=font, anchor=anchor, **kwargs)

def create_frame(master, fg_color=None, **kwargs):
    return ctk.CTkFrame(master, fg_color=fg_color, **kwargs)

def get_subtitle_font():
    return ("Arial", 12, "bold")

def get_card_title_font():
    return ("Arial", 14, "bold")

def get_card_detail_font():
    return ("Arial", 12)

def get_card_icon_font():
    return ("Arial", 12)

class PetCardWithRecords(ctk.CTkFrame):
    def __init__(self, master, pet, image_store, owner=None, on_click=None, *args, **kwargs):
        self.pet = pet
        self.owner = owner
        self.image_store = image_store
        self.on_click = on_click
        self.vaccinations = VaccinationController().get_by_pet_id(pet.id)
        self.vet_visits = VetVisitController().get_by_pet_id(pet.id)

        # Generate a random pastel color for the card background
        self._pastel_color = self.generate_pastel_color()
        super().__init__(
            master,
            fg_color=self._pastel_color,
            corner_radius=16,
            border_width=2,
            border_color="#e0e0e0",
            *args,
            **kwargs
        )
        self.configure(width=260)
        self.columnconfigure(0, weight=1)
        self._original_fg_color = self._pastel_color
        self._build_card()
        self._bind_recursive(self)

    def _bind_recursive(self, widget):
        widget.bind("<Button-1>", self._handle_click)
        # Bind hover events to all widgets
        def on_enter(e):
            self.configure(border_color="#3b8ed0", fg_color="#d1e8ff")  # Light blue pastel color on hover
        def on_leave(e):
            self.configure(border_color="#e0e0e0", fg_color=self._original_fg_color)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        for child in widget.winfo_children():
            self._bind_recursive(child)

    def _handle_click(self, event):
        if self.on_click:
            self.on_click(self.pet)

    @staticmethod
    def generate_pastel_color():
        base_color = random.randint(200, 230)
        red = base_color + random.randint(0, 55)
        green = base_color + random.randint(0, 55)
        blue = base_color + random.randint(0, 55)
        red = min(255, red)
        green = min(255, green)
        blue = min(255, blue)
        return f"#{red:02x}{green:02x}{blue:02x}"

    def _get_pet_thumbnail(self):
        try:
            if not self.pet.image_path:
                raise FileNotFoundError
            img_path = os.path.join("backend", "data", self.pet.image_path)
            if not os.path.exists(img_path):
                raise FileNotFoundError
            image = Image.open(img_path).resize((140, 140))
            thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
            self.image_store.append(thumb)
            return thumb
        except Exception:
            try:
                fallback_path = os.path.join("frontend", "assets", "no-pet-image.png")
                if os.path.exists(fallback_path):
                    image = Image.open(fallback_path).resize((140, 140))
                    thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
                    self.image_store.append(thumb)
                    self._missing_image = True
                    return thumb
            except Exception:
                pass
            image = Image.new("RGB", (140, 140), color="lightgray")
            thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
            self.image_store.append(thumb)
            self._missing_image = True
            return thumb

    def _build_card(self):
        container = create_frame(self, self._original_fg_color)
        container.pack(padx=12, pady=12, fill="both", expand=True)

        main_row = create_frame(container)
        main_row.configure(fg_color=self._original_fg_color)
        main_row.pack(fill="both", expand=True)

        # Left: Info Section
        info_frame = create_frame(main_row)
        info_frame.configure(fg_color=self._original_fg_color)
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        name_frame = create_frame(info_frame)
        name_frame.configure(fg_color=self._original_fg_color)
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

        details_frame = create_frame(info_frame)
        details_frame.configure(fg_color=self._original_fg_color)
        details_frame.pack(fill="x", padx=8)

        breed_row = create_frame(details_frame)
        breed_row.configure(fg_color=self._original_fg_color)
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

        birth_row = create_frame(details_frame)
        birth_row.configure(fg_color=self._original_fg_color)
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

        age_row = create_frame(details_frame)
        age_row.configure(fg_color=self._original_fg_color)
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

        if self.owner:
            owner_row = create_frame(details_frame)
            owner_row.configure(fg_color=self._original_fg_color)
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

        # Right: Image Section
        image_frame = create_frame(main_row)
        image_frame.configure(fg_color=self._original_fg_color)
        image_frame.pack(side="right", fill="y", padx=(10, 0))
        thumbnail = self._get_pet_thumbnail()
        label_image = ctk.CTkLabel(
            image_frame,
            image=thumbnail,
            text="",
            compound="top"
        )
        label_image.pack(anchor="center", pady=5)
        if hasattr(self, '_missing_image') and self._missing_image:
            ctk.CTkLabel(
                image_frame,
                text="Oh no! I can't see your pet's cuteness",
                font=get_card_detail_font(),
                text_color="#888888"
            ).pack(pady=(8, 0))

        # Below: Vaccination and Vet Visit Records Section
        records_frame = create_frame(container)
        records_frame.configure(fg_color=self._original_fg_color)
        records_frame.pack(fill="x", pady=(10, 0))

        vacc_label = create_label(records_frame, "Vaccinations:", font=get_subtitle_font())
        vacc_label.pack(anchor="w")
        if self.vaccinations:
            for v in self.vaccinations:
                create_label(records_frame, f"• {v}", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)
        else:
            create_label(records_frame, "No vaccinations.", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)

        visit_label = create_label(records_frame, "Vet Visits:", font=get_subtitle_font())
        visit_label.pack(anchor="w", pady=(8, 0))
        if self.vet_visits:
            for v in self.vet_visits:
                create_label(records_frame, f"• {v}", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)
        else:
            create_label(records_frame, "No vet visits.", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)


