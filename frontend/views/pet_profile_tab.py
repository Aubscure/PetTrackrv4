import customtkinter as ctk
from PIL import Image
import os
from frontend.components.copyright import get_copyright_label
from frontend.style.style import (
    create_label1, create_frame, create_button,
    get_title_font, get_subtitle_font, get_card_detail_font
)
from backend.services.daycare_prices import compute_total_fee

class PetProfileTab:
    def __init__(self, parent, pet, owner, vet_visits, vaccinations, feeding_logs, grooming_logs, show_frame, go_back):
        self.parent = parent
        self.pet = pet
        self.owner = owner
        self.vet_visits = vet_visits
        self.vaccinations = vaccinations
        self.feeding_logs = feeding_logs
        self.grooming_logs = grooming_logs
        self.show_frame = show_frame
        self.go_back = go_back
        self._build()

    def _build(self):
        self._clear_parent()
        self._setup_main_layout()

    def _clear_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parent.pack_propagate(False)

    def _setup_main_layout(self):
        # Outer wrapper to hold everything vertically
        outer_frame = ctk.CTkFrame(self.parent, fg_color="white")
        outer_frame.pack(fill="both", expand=True)
        outer_frame.pack_propagate(False)

        # Optional top spacer
        ctk.CTkFrame(outer_frame, height=20, fg_color="white").pack(fill="x")

        # Main content
        main = ctk.CTkFrame(outer_frame, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=80, pady=(0, 0))
        main.grid_columnconfigure(0, weight=1, minsize=340)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self._image_panel(main)
        self._content_panel(main)

        # Back button
        btn = create_button(
            outer_frame,
            text="← Back",
            command=self.go_back if self.go_back else lambda: self.show_frame("view_pets"),
            color="#8c8c8c",
            width=120
        )
        btn.pack(pady=(8, 4))

        # Copyright at very bottom
        copyright_label = get_copyright_label(outer_frame)
        copyright_label.pack(side="bottom", pady=(4, 6))


    def _image_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="#f0f8ff", corner_radius=16, border_width=2, border_color="#4a90d9")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        panel.grid_propagate(False)
        panel.configure(width=340, height=420)

        img = self._get_image()
        image_label = ctk.CTkLabel(panel, image=ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300)), text="")
        image_label.pack(pady=(20, 10))

        create_label1(panel, f"🐾 {self.pet.name}'s Profile", font=get_title_font(), justify="center").pack(pady=(0, 8))

        # Pet and Owner Details in Image Panel
        info_frame = ctk.CTkFrame(panel, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)

        create_label1(info_frame, f"🐶 Breed: {self.pet.breed or 'Unknown'}", font=get_card_detail_font(), justify="center").pack(pady=5)
        create_label1(info_frame, f"🎂 Birthdate: {self.pet.birthdate}", font=get_card_detail_font(), justify="center").pack(pady=5)
        create_label1(info_frame, f"📅 Age: {self.pet.age()}", font=get_card_detail_font(), justify="center").pack(pady=5)

        if self.owner:
            create_label1(info_frame, f"👤 Owner: {self.owner.name}", font=get_card_detail_font(), justify="center").pack(pady=5)
            create_label1(info_frame, f"📞 Contact: {self.owner.contact_number}", font=get_card_detail_font(), justify="center").pack(pady=5)
            create_label1(info_frame, f"🏠 Address: {self.owner.address}", font=get_card_detail_font(), justify="center").pack(pady=5)

    def _get_image(self):
        try:
            img_path = os.path.join("backend", "data", getattr(self.pet, 'image_path', "")) if hasattr(self.pet, 'image_path') else None
            return Image.open(img_path).resize((300, 300)) if img_path and os.path.exists(img_path) else Image.new("RGB", (300, 300), "#4a90d9")
        except Exception:
            return Image.new("RGB", (300, 300), "#4a90d9")

    def _content_panel(self, parent):
        scrollable_frame = ctk.CTkScrollableFrame(parent, fg_color="#f5f7fa", corner_radius=18, border_width=2, border_color="#d0d4db")
        scrollable_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        content = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=24, pady=24)

        self._records_section(content, "🩺 Vet Visits", self.vet_visits, self._vet_visit_item, top=0)
        self._records_section(content, "💉 Vaccinations", self.vaccinations, self._vaccine_item, top=20, empty="No vaccination records available")
        self._records_section(content, "🍖 Feeding Logs", self.feeding_logs, self._feeding_item, top=20, empty="No feeding records available")
        self._records_section(content, "✂️ Grooming Logs", self.grooming_logs, self._grooming_item, top=20, empty="No grooming records available")

    def _records_section(self, parent, title, records, item_fn, top=0, empty=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(top, 0))

        create_label1(frame, title, font=get_subtitle_font(), justify="left").pack(anchor="w", pady=(0, 12))

        if records:
            for rec in records:
                item_fn(frame, rec)
        elif empty:
            self._create_empty_state(frame, empty)

    def _vet_visit_item(self, parent, visit):
        self._create_record_item(
            parent, icon="📅",
            main_text=f"{visit.visit_date}: {visit.reason}",
            secondary_text=f"💰 ₱{getattr(visit, 'cost', 0):,.2f}",
            notes=getattr(visit, 'notes', None)
        )

    def _vaccine_item(self, parent, vaccine):
        self._create_record_item(
            parent, icon="🦠",
            main_text=getattr(vaccine, 'vaccine_name', 'Unknown vaccine'),
            secondary_text=f"💰 ₱{getattr(vaccine, 'price', 0):,.2f}",
            details=[
                f"🗓️ Administered: {getattr(vaccine, 'date_administered', 'Unknown date')}",
                f"🔜 Next Due: {getattr(vaccine, 'next_due', 'Unknown date')}"
            ]
        )

    def _feeding_item(self, parent, log):
        plan = ", ".join([p for p, cond in [
            ("Once a day", getattr(log, 'feed_once', False)),
            ("Twice a day", getattr(log, 'feed_twice', False)),
            ("Thrice a day", getattr(log, 'feed_thrice', False))
        ] if cond]) or "No specific plan"
        total_fee = compute_total_fee(
            getattr(log, 'num_days', 0),
            getattr(log, 'feed_once', False),
            getattr(log, 'feed_twice', False),
            getattr(log, 'feed_thrice', False)
        )
        self._create_record_item(
            parent,
            icon="📅",
            main_text=f"{getattr(log, 'start_date', 'Unknown date')} — {getattr(log, 'num_days', '?')} day(s)",
            secondary_text=f"Plan: {plan} | Total Fee: ₱{total_fee:,}",
            notes=getattr(log, 'notes', None)
        )

    def _grooming_item(self, parent, grooming):
        groom_type_map = {
            "basic": "Basic Groom",
            "premium": "Premium Groom",
            "custom": "Custom Groom"
        }
        groom_type_label = groom_type_map.get(getattr(grooming, "groom_type", ""), grooming.groom_type.capitalize())
        self._create_record_item(
            parent,
            icon="✂️",
            main_text=f"{getattr(grooming, 'groom_date', 'Unknown date')}: {groom_type_label}",
            secondary_text=f"💰 ₱{getattr(grooming, 'price', 0):,.2f} by {getattr(grooming, 'groomer_name', 'Unknown')}",
            notes=getattr(grooming, 'notes', None)
        )

    def _create_record_item(self, parent, icon, main_text, secondary_text=None, details=None, notes=None):
        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.pack(fill="x", pady=(0, 12))

        icon_label = ctk.CTkLabel(item, text=icon, font=("Arial", 16), fg_color="transparent")
        icon_label.pack(side="left", padx=(0, 12))

        text_frame = ctk.CTkFrame(item, fg_color="transparent")
        text_frame.pack(fill="x", expand=True)

        main_label = create_label1(text_frame, main_text, font=get_card_detail_font(), text_color="#222")
        main_label.pack(anchor="w")

        if secondary_text:
            secondary_label = create_label1(text_frame, secondary_text, font=get_card_detail_font(), text_color="#666")
            secondary_label.pack(anchor="w")

        if details:
            for detail in details:
                detail_label = create_label1(text_frame, detail, font=get_card_detail_font(), text_color="#888")
                detail_label.pack(anchor="w")

        if notes:
            notes_label = create_label1(text_frame, f"📝 Notes: {notes}", font=get_card_detail_font(), text_color="#888")
            notes_label.pack(anchor="w")

        separator = ctk.CTkFrame(parent, height=1, fg_color="#e0e0e0")
        separator.pack(fill="x", pady=(8, 0))

    def _create_empty_state(self, parent, text):
        empty_frame = ctk.CTkFrame(parent, fg_color="transparent")
        empty_frame.pack(fill="x", pady=(0, 12))

        create_label1(empty_frame, text, font=get_card_detail_font(), text_color="#888", justify="center").pack()

    def _back_button(self):
        btn = create_button(
            self.parent,
            text="← Back",
            command=self.go_back if self.go_back else lambda: self.show_frame("view_pets"),
            color="#8c8c8c",
            width=120
        )
        btn.pack(side="bottom", pady=16)


def create_pet_profile_tab(parent, pet, owner, vet_visits, vaccinations, feeding_logs, grooming_logs, show_frame, go_back=None):
    """
    Factory function to create and display a PetProfileTab.
    """
    PetProfileTab(parent, pet, owner, vet_visits, vaccinations, feeding_logs, grooming_logs, show_frame, go_back)
    return parent

