import os
import random
from PIL import Image
import customtkinter as ctk
from backend.controllers.grooming_controller import GroomingLogsController
from frontend.style.style import (
    create_label,
    create_frame,
    get_subtitle_font,
    get_card_detail_font,
    get_card_title_font,
    get_card_icon_font,
)

class PetCardWithGroomingLogs(ctk.CTkFrame):
    def __init__(self, master, pet, image_store, owner=None, on_click=None, *args, **kwargs):
        self.pet = pet
        self.owner = owner
        self.image_store = image_store
        self.on_click = on_click
        self.grooming_logs = GroomingLogsController().get_grooming_logs_for_pet(pet.id)

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
        def on_enter(e):
            self.configure(border_color="#3b8ed0", fg_color="#d1e8ff")
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
        base = random.randint(200, 230)
        r = min(255, base + random.randint(0, 55))
        g = min(255, base + random.randint(0, 55))
        b = min(255, base + random.randint(0, 55))
        return f"#{r:02x}{g:02x}{b:02x}"

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

        main_row = create_frame(container, self._original_fg_color)
        main_row.pack(fill="both", expand=True)

        info_frame = create_frame(main_row, self._original_fg_color)
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        name_frame = create_frame(info_frame, self._original_fg_color)
        name_frame.pack(pady=(0, 8), anchor="w")
        ctk.CTkLabel(name_frame, text="🐾", font=get_card_icon_font()).pack(side="left", padx=(0, 5))
        create_label(name_frame, self.pet.name, font=get_card_title_font()).pack(side="left")

        details_frame = create_frame(info_frame, self._original_fg_color)
        details_frame.pack(fill="x", padx=8)

        for icon, value in [
            ("🐶", self.pet.breed or "Unknown"),
            ("📅", self.pet.birthdate),
            ("🕒", self.pet.age())
        ]:
            row = create_frame(details_frame, self._original_fg_color)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=icon, font=get_card_icon_font(), width=24, anchor="w").pack(side="left")
            create_label(row, value, font=get_card_detail_font(), anchor="w").pack(side="left", padx=5)

        if self.owner:
            owner_row = create_frame(details_frame, self._original_fg_color)
            owner_row.pack(fill="x", pady=3)
            ctk.CTkLabel(owner_row, text="👤", font=get_card_icon_font(), width=24, anchor="w").pack(side="left")
            create_label(
                owner_row,
                f"{self.owner.name} ({self.owner.contact_number})",
                font=get_card_detail_font(),
                anchor="w"
            ).pack(side="left", padx=5)

        image_frame = create_frame(main_row, self._original_fg_color)
        image_frame.pack(side="right", fill="y", padx=(10, 0))
        thumbnail = self._get_pet_thumbnail()
        ctk.CTkLabel(image_frame, image=thumbnail, text="", compound="top").pack(anchor="center", pady=5)

        if hasattr(self, '_missing_image') and self._missing_image:
            ctk.CTkLabel(
                image_frame,
                text="Oh no! I can't see your pet's cuteness",
                font=get_card_detail_font(),
                text_color="#888888"
            ).pack(pady=(8, 0))

        logs_frame = create_frame(container, self._original_fg_color)
        logs_frame.pack(fill="x", pady=(10, 0))

        create_label(logs_frame, "Grooming Logs:", font=get_subtitle_font()).pack(anchor="w")
        if self.grooming_logs:
            for log in self.grooming_logs:
                log_row = create_frame(logs_frame, self._original_fg_color)
                log_row.pack(fill="x", padx=5, pady=2)
                create_label(
                    log_row,
                    f"• {log}",
                    font=get_card_detail_font(),
                    anchor="w",
                    wraplength=400
                ).pack(fill="x", anchor="w")
        else:
            create_label(
                logs_frame,
                "No grooming logs.",
                font=get_card_detail_font(),
                anchor="w"
            ).pack(anchor="w", padx=10)
