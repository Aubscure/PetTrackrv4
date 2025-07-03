import os
import random
from PIL import Image
import customtkinter as ctk
from frontend.style.style import (
    create_label,
    create_frame,
    get_subtitle_font,
    get_card_title_font,
    get_card_detail_font,
    get_card_icon_font
)

def generate_pastel_color():
    # Generate a random pastel color
    base_color = random.randint(200, 230)  # Base value for pastel colors
    red = base_color + random.randint(0, 55)
    green = base_color + random.randint(0, 55)
    blue = base_color + random.randint(0, 55)
    # Ensure the values are within the valid range
    red = min(255, red)
    green = min(255, green)
    blue = min(255, blue)
    # Convert to hex color code
    return f"#{red:02x}{green:02x}{blue:02x}"

class PetCard(ctk.CTkFrame):

    def __init__(self, master, pet, image_store, owner=None, on_click=None, *args, **kwargs):
        # Generate a random pastel color for the card background
        pastel_color = generate_pastel_color()
        super().__init__(
            master,
            fg_color=pastel_color,  # Use the generated pastel color
            corner_radius=16,
            border_width=2,
            border_color="#e0e0e0",
            *args,
            **kwargs
        )
        self.pet = pet
        self.owner = owner
        self.image_store = image_store
        self.on_click = on_click
        self.configure(width=260)
        self.columnconfigure(0, weight=1)
        self._original_fg_color = pastel_color  # Save the original color for hover effects
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
            self.on_click(self.pet, self.owner)

    def _build_card(self):
        # Main container with consistent padding
        container = create_frame(self, self._original_fg_color)  # Use the same pastel color for the container
        container.pack(padx=12, pady=12, fill="both", expand=True)

        # Image section - larger and centered
        thumbnail = self._get_pet_thumbnail()
        image_frame = create_frame(container, self._original_fg_color)
        image_frame.pack(pady=(0, 10))

        label_image = ctk.CTkLabel(
            image_frame,
            image=thumbnail,
            text="",
            compound="top"
        )
        label_image.pack()
        # Show message if image is missing
        if hasattr(self, '_missing_image') and self._missing_image:
            ctk.CTkLabel(
                image_frame,
                text="Oh no! I can't see your pet's cuteness",
                font=get_card_detail_font(),
                text_color="#888888"
            ).pack(pady=(8, 0))

        # Info section
        info_frame = create_frame(container, self._original_fg_color)
        info_frame.pack(fill="x")

        # Name with larger font and paw emoji
        name_frame = create_frame(info_frame, self._original_fg_color)
        name_frame.pack(pady=(0, 8))
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
        details_frame = create_frame(info_frame, self._original_fg_color)
        details_frame.pack(fill="x", padx=8)

        # Breed row
        breed_row = create_frame(details_frame, self._original_fg_color)
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
        birth_row = create_frame(details_frame, self._original_fg_color)
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
        age_row = create_frame(details_frame, self._original_fg_color)
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
            owner_row = create_frame(details_frame, self._original_fg_color)
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

    def _get_pet_thumbnail(self):
        try:
            if not self.pet.image_path:
                raise FileNotFoundError
            img_path = os.path.join("backend", "data", self.pet.image_path)
            if not os.path.exists(img_path):
                raise FileNotFoundError
            image = Image.open(img_path).resize((140, 140))  # Larger image
            thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
            self.image_store.append(thumb)
            return thumb
        except Exception:
            # Try to use the fallback image
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
            # Fallback to blank/gray image
            image = Image.new("RGB", (140, 140), color="lightgray")
            thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
            self.image_store.append(thumb)
            self._missing_image = True
            return thumb
