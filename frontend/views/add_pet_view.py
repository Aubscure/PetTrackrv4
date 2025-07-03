# frontend/views/add_pet_view.py
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
from backend.models.pet import Pet, Owner
from backend.models.vet_visit import VetVisit
from backend.models.vaccination import Vaccination
from backend.models.feeding_log import FeedingLog
from backend.controllers.pet_controller import PetController
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController
from frontend.components.floating_placeholder_entry import FloatingPlaceholderEntry
from frontend.components.copyright import get_copyright_label
from frontend.components.image_uploader import ImageUploader
from frontend.style.style import (
    create_button, create_label, create_frame, 
    get_title_font, get_subtitle_font, create_back_button
)
from backend.services.daycare_prices import compute_total_fee
import os  # Add this import at the top if not present

class AddPetView:
    VACCINE_NAMES = ["Rabies", "Distemper", "Bordetella", "Parvo"]
    PLAN_OPTIONS = [("Once a day", "1"), ("Twice a day", "2"), ("Thrice a day", "3"), ("No feeding", "4")]
    VET_VISIT_REASONS = [
        "Checkup", "Vaccination", "Dental Cleaning", "Injury Treatment", "Surgery",
        "Skin Problem", "Eye/Ear Issue", "Digestive Issue", "Post-Op Follow-up", "Other"
    ]
    GROOM_TYPES = [
        ("Basic Groom (₱1,000)", "basic"),
        ("Premium Groom (₱1,800)", "premium"),
        ("Custom Groom (₱1,500)", "custom"),
    ]

    def __init__(self, parent, show_frame):
        self.parent = parent
        self.show_frame = show_frame
        self.records = {"vet_visits": [], "vaccinations": [], "feeding_logs": [], "groomings": []}
        self._build_ui()

    def _build_ui(self):
        for w in self.parent.winfo_children(): w.destroy()
        container = create_frame(self.parent)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
        container.grid_columnconfigure((0, 1), weight=1)
        create_label(container, "➕ Add New Pet", font=get_title_font()).grid(row=0, column=0, columnspan=2, pady=(30, 15))

        # Left: Image (fixed height, does not expand)
        left = create_frame(container)
        left.grid(row=1, column=0, padx=20, pady=10, sticky="n")  # Only sticky to north (top)
        left.configure(height=380)  # Set a fixed height for the container
        left.grid_propagate(False)  # Prevent the frame from resizing to its content

        self.image_uploader = ImageUploader(left)
        self.image_uploader.pack(pady=(0, 10), fill="both", expand=True)  # This is fine, as left is fixed

        # Right: Tabs (expands)
        right = create_frame(container)
        right.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)
        notebook = ctk.CTkTabview(right)
        notebook.pack(padx=10, pady=10, fill="both", expand=True)
        self._build_pet_tab(notebook.add("Pet Details"))
        self._build_owner_tab(notebook.add("Owner Details"))
        self._build_medical_tab(notebook.add("Medical Records"))

        btn_frame = create_frame(right)
        btn_frame.pack(pady=(10, 30), fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="buttons")
        create_back_button(btn_frame, text="BACK", command=lambda: self.show_frame("dashboard"), width=100).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        create_button(btn_frame, text="SAVE", command=self.save_pet, width=100).grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def _build_pet_tab(self, tab):
        self.name_entry = FloatingPlaceholderEntry(tab, "Pet Name")
        self.breed_entry = FloatingPlaceholderEntry(tab, "Breed (optional)")
        for e in (self.name_entry, self.breed_entry): e.pack(pady=8, fill="x")
        bdate_frame = create_frame(tab)
        bdate_frame.pack(pady=8, fill="x")
        create_label(bdate_frame, "Birthdate", font=get_subtitle_font()).pack(anchor="w")
        self.bdate_entry = DateEntry(bdate_frame, width=26, date_pattern="yyyy-mm-dd", background="#3b8ed0", foreground="white", borderwidth=2)
        self.bdate_entry.pack(pady=8, ipady=4, fill="x")

    def _build_owner_tab(self, tab):
        self.owner_name_entry = FloatingPlaceholderEntry(tab, "Owner Name")
        self.owner_phone_entry = FloatingPlaceholderEntry(tab, "Contact Number")
        self.owner_address_entry = FloatingPlaceholderEntry(tab, "Address")
        for e in (self.owner_name_entry, self.owner_phone_entry, self.owner_address_entry): e.pack(pady=8, fill="x")

    def _build_medical_tab(self, tab):
        notebook = ctk.CTkTabview(tab)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        self.vet_entries = self._vet_visit_section(notebook.add("Vet Visits"))
        self.vax_entries = self._vaccination_section(notebook.add("Vaccinations"))
        self.feed_entries, _ = self._feeding_section(notebook.add("Feeding Logs"))
        self.groom_entries = self._grooming_section(notebook.add("Grooming Logs"))  # NEW
        self._add_record_buttons(notebook)

    def _vet_visit_section(self, tab):
        from customtkinter import CTkComboBox
        entries = {}
        # Visit Date
        frame_date = create_frame(tab); frame_date.pack(pady=5, fill="x")
        create_label(frame_date, "Visit Date", font=get_subtitle_font()).pack(anchor="w")
        visit_date_entry = DateEntry(frame_date, width=26, date_pattern="yyyy-mm-dd", background="#3b8ed0", foreground="white", borderwidth=2)
        visit_date_entry.pack(pady=5, fill="x")
        entries["visit_date"] = visit_date_entry

        # Reason (Dropdown)
        frame_reason = create_frame(tab); frame_reason.pack(pady=5, fill="x")
        create_label(frame_reason, "Reason for Visit", font=get_subtitle_font()).pack(anchor="w")
        reason_cb = CTkComboBox(frame_reason, values=self.VET_VISIT_REASONS, width=220)
        reason_cb.pack(pady=5, fill="x")
        reason_cb.set(self.VET_VISIT_REASONS[0])
        entries["reason"] = reason_cb

        # Notes
        notes_entry = ctk.CTkTextbox(tab, height=80, wrap="word")
        notes_entry.pack(pady=8, fill="x")
        notes_entry.insert("0.0", "Notes (optional)")
        notes_entry.bind("<FocusIn>", lambda e, w=notes_entry: w.delete("0.0", "end") if w.get("0.0", "end").strip() == "Notes (optional)" else None)
        entries["notes"] = notes_entry

        # Cost (accepts float or int)
        frame_cost = create_frame(tab); frame_cost.pack(pady=5, fill="x")
        create_label(frame_cost, "Cost (₱)", font=get_subtitle_font()).pack(anchor="w")
        cost_var = ctk.StringVar()
        cost_entry = ctk.CTkEntry(frame_cost, textvariable=cost_var)
        cost_entry.pack(pady=5, fill="x")
        entries["cost"] = cost_entry

        # Validation for cost: only allow float/int
        def validate_cost(*_):
            val = cost_var.get()
            if val == "":
                cost_entry.configure(border_color="#3b8ed0")
                return
            try:
                float(val)
                cost_entry.configure(border_color="#3b8ed0")
            except ValueError:
                cost_entry.configure(border_color="red")
        cost_var.trace_add("write", lambda *_: validate_cost())

        return entries

    def _vaccination_section(self, tab):
        from customtkinter import CTkComboBox
        entries = {}
        frame1 = create_frame(tab); frame1.pack(pady=5, fill="x")
        create_label(frame1, "Vaccine Name", font=get_subtitle_font()).pack(anchor="w")
        vaccine_name_cb = CTkComboBox(frame1, values=self.VACCINE_NAMES, width=220)
        vaccine_name_cb.pack(pady=5, fill="x")
        entries["vaccine_name"] = vaccine_name_cb
        price_var = ctk.StringVar(value="₱0")
        create_label(frame1, "Price", font=get_subtitle_font()).pack(anchor="w")
        ctk.CTkLabel(frame1, textvariable=price_var).pack(pady=2, fill="x")
        entries["price_var"] = price_var
        def update_price(*_):
            price = Vaccination.VACCINE_PRICES.get(vaccine_name_cb.get(), 0)
            price_var.set(f"₱{price}")
        vaccine_name_cb.configure(command=lambda _: update_price())
        vaccine_name_cb.set(self.VACCINE_NAMES[0]); update_price()
        frame2 = create_frame(tab); frame2.pack(pady=5, fill="x")
        create_label(frame2, "Date Administered", font=get_subtitle_font()).pack(anchor="w")
        date_admin_entry = DateEntry(frame2, width=26, date_pattern="yyyy-mm-dd", background="#3b8ed0", foreground="white", borderwidth=2)
        date_admin_entry.pack(pady=5, fill="x")
        entries["date_administered"] = date_admin_entry
        frame3 = create_frame(tab); frame3.pack(pady=5, fill="x")
        create_label(frame3, "Next Due Date (auto)", font=get_subtitle_font()).pack(anchor="w")
        next_due_var = ctk.StringVar(value="")
        ctk.CTkLabel(frame3, textvariable=next_due_var, font=get_subtitle_font()).pack(pady=5, fill="x")
        entries["next_due_var"] = next_due_var
        notes_entry = ctk.CTkTextbox(tab, height=80, wrap="word")
        notes_entry.pack(pady=8, fill="x")
        notes_entry.insert("0.0", "Notes (optional)")
        entries["notes"] = notes_entry
        def update_next_due(*_):
            try:
                vax = Vaccination(0, vaccine_name_cb.get(), date_admin_entry.get(), "")
                next_due_var.set(vax.next_due)
            except: next_due_var.set("")
        vaccine_name_cb.bind("<<ComboboxSelected>>", lambda e: update_next_due())
        date_admin_entry.bind("<<DateEntrySelected>>", lambda e: update_next_due())
        date_admin_entry.bind("<FocusOut>", lambda e: update_next_due())
        return entries

    def _feeding_section(self, tab):
        entries = {}
        scroll = ctk.CTkScrollableFrame(tab, height=340)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        top = create_frame(scroll); top.pack(pady=(0, 16), fill="x")
        create_label(top, "Start Date", font=get_subtitle_font()).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 0))
        start_date = DateEntry(top, width=18, date_pattern="yyyy-mm-dd", background="#3b8ed0", foreground="white", borderwidth=2)
        start_date.grid(row=0, column=1, sticky="ew")
        create_label(top, "Number of Days", font=get_subtitle_font()).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        num_days = FloatingPlaceholderEntry(top, "e.g. 3")
        num_days.grid(row=1, column=1, sticky="ew", pady=(10, 0))
        entries["start_date"], entries["num_days"] = start_date, num_days
        top.grid_columnconfigure(1, weight=1)
        plan_frame = create_frame(scroll); plan_frame.pack(pady=(0, 16), fill="x")
        create_label(plan_frame, "Feeding Plan", font=get_subtitle_font()).pack(anchor="w", pady=(0, 6))
        plan_var = ctk.StringVar(value="1")
        for t, v in self.PLAN_OPTIONS:
            ctk.CTkRadioButton(plan_frame, text=t, variable=plan_var, value=v).pack(anchor="w", padx=10, pady=2)
        entries["plan_var"] = plan_var
        price_label = create_label(scroll, "Total Fee: ₱0", font=get_subtitle_font())
        price_label.pack(pady=(0, 16), anchor="w")
        def update_price(*_):
            try:
                days = int(num_days.get())
                plan = plan_var.get()
                total = compute_total_fee(days, plan == "1", plan == "2", plan == "3")
                price_label.configure(text=f"Total Fee: ₱{total}")
            except: price_label.configure(text="Total Fee: ₱0")
        num_days.bind("<KeyRelease>", lambda e: update_price())
        plan_var.trace_add("write", lambda *_: update_price())
        create_label(scroll, "Notes (optional)", font=get_subtitle_font()).pack(anchor="w", pady=(0, 6))
        notes_entry = ctk.CTkTextbox(scroll, height=60, wrap="word")
        notes_entry.pack(pady=(0, 10), fill="x")
        entries["notes"] = notes_entry
        return entries, price_label

    def _grooming_section(self, tab):
        from customtkinter import CTkRadioButton, StringVar
        entries = {}
        # Groom Type Radios
        create_label(tab, "Groom Type", font=get_subtitle_font()).pack(anchor="w", pady=(0, 6))
        groom_type_var = ctk.StringVar(value="basic")
        for label, value in self.GROOM_TYPES:
            ctk.CTkRadioButton(tab, text=label, variable=groom_type_var, value=value).pack(anchor="w", padx=10, pady=2)
        entries["groom_type"] = groom_type_var

        # Groomer Name
        entries["groomer_name"] = FloatingPlaceholderEntry(tab, "Groomer Name")
        entries["groomer_name"].pack(pady=8, fill="x")

        # Notes
        notes_entry = ctk.CTkTextbox(tab, height=60, wrap="word")
        notes_entry.pack(pady=8, fill="x")
        notes_entry.insert("0.0", "Notes (optional)")
        entries["notes"] = notes_entry

        return entries

    def _add_record_buttons(self, notebook):
        tab_map = {
            "vet_visits": self.vet_entries,
            "vaccinations": self.vax_entries,
            "feeding_logs": self.feed_entries,
            "groomings": self.groom_entries,  # NEW
        }
        tab_names = {
            "vet_visits": "Vet Visits",
            "vaccinations": "Vaccinations",
            "feeding_logs": "Feeding Logs",
            "groomings": "Grooming Logs",  # NEW
        }
        required_fields = {
            "vet_visits": ["visit_date", "reason"],
            "vaccinations": ["vaccine_name", "date_administered", "next_due"],
            "feeding_logs": [],
            "groomings": ["groom_type", "groomer_name"],  # NEW
        }
        success_msgs = {
            "vet_visits": "Vet visit added successfully!",
            "vaccinations": "Vaccination added successfully!",
            "feeding_logs": "Feeding log added successfully!",
            "groomings": "Grooming log added successfully!",  # NEW
        }
        for record_type in tab_map:
            tab = notebook.tab(tab_names[record_type])
            create_button(tab, text=f"➕ Add {tab_names[record_type][:-1]}",
                command=lambda rt=record_type: self.add_record(rt, tab_map[rt], required_fields[rt], success_msgs[rt]), width=120
            ).pack(pady=10)

    def add_record(self, record_type, entries, required_fields, success_msg):
        data = {}
        if record_type == "feeding_logs":
            try:
                data["start_date"] = entries["start_date"].get()
                data["num_days"] = int(entries["num_days"].get())
                plan = entries["plan_var"].get()
                data["feed_once"], data["feed_twice"], data["feed_thrice"] = plan == "1", plan == "2", plan == "3"
                data["notes"] = entries["notes"].get("0.0", "end").strip()
                total = compute_total_fee(data["num_days"], data["feed_once"], data["feed_twice"], data["feed_thrice"])
                plan_desc = "Once a day" if data["feed_once"] else "Twice a day" if data["feed_twice"] else "Thrice a day" if data["feed_thrice"] else "No feeding"
                addon = 85 if data["feed_once"] else 170 if data["feed_twice"] else 255 if data["feed_thrice"] else 0
                breakdown = f"Plan: {plan_desc}\nBreakdown: {data['num_days']} x (₱350 base + ₱{addon} feeding) = ₱{total}"
                messagebox.showinfo("Feeding Log Added", f"{success_msg}\n\n{breakdown}")
                self.records[record_type].append(data)
            except Exception as e:
                messagebox.showwarning("Invalid Input", f"Please fill all required fields correctly.\n\n{e}")
        elif record_type == "vet_visits":
            # Custom handling for vet visits
            data["visit_date"] = entries["visit_date"].get()
            data["reason"] = entries["reason"].get()
            data["notes"] = entries["notes"].get("0.0", "end").strip()
            cost_val = entries["cost"].get()
            try:
                data["cost"] = float(cost_val) if cost_val else 0.0
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for cost.")
                return
            if not all(data.get(f) for f in ["visit_date", "reason"]):
                messagebox.showwarning("Missing Info", "Please fill all required fields.")
                return
            self.records[record_type].append(data)
            messagebox.showinfo("Added", success_msg)
            # Reset fields
            for key, entry in entries.items():
                if key == "notes":
                    entry.delete("0.0", "end")
                    entry.insert("0.0", "Notes (optional)")
                elif key == "visit_date":
                    entry.set_date(datetime.now())
                elif key == "reason":
                    entry.set(self.VET_VISIT_REASONS[0])
                elif key == "cost":
                    entry.delete(0, "end")
        elif record_type == "groomings":
            data = {}
            data["groom_type"] = entries["groom_type"].get()
            data["groomer_name"] = entries["groomer_name"].get()
            data["notes"] = entries["notes"].get("0.0", "end").strip()
            # Set price based on type
            price_map = {"basic": 1000.0, "custom": 1500.0, "premium": 1800.0}
            data["price"] = price_map.get(data["groom_type"], 0.0)
            if not all(data.get(f) for f in required_fields):
                messagebox.showwarning("Missing Info", "Please fill all required fields.")
                return
            self.records[record_type].append(data)
            messagebox.showinfo("Added", success_msg)
            # Reset fields
            entries["groom_type"].set("basic")
            entries["groomer_name"].delete(0, "end")
            entries["notes"].delete("0.0", "end")
            entries["notes"].insert("0.0", "Notes (optional)")
        else:
            for name, entry in entries.items():
                if name in ("next_due_var", "price_var"): continue
                if hasattr(entry, "get"):
                    data[name] = entry.get("0.0", "end").strip() if isinstance(entry, ctk.CTkTextbox) else entry.get()
            if record_type == "vaccinations":
                data["next_due"] = entries["next_due_var"].get()
                data["price"] = Vaccination.VACCINE_PRICES.get(entries["vaccine_name"].get(), 0)
            if not all(data.get(f) for f in required_fields):
                messagebox.showwarning("Missing Info", "Please fill all required fields.")
                return
            self.records[record_type].append(data)
            messagebox.showinfo("Added", success_msg)
            for entry in entries.values():
                if isinstance(entry, ctk.CTkTextbox):
                    entry.delete("0.0", "end")
                    entry.insert("0.0", "Notes (optional)" if record_type != "feeding_logs" else "")
                elif isinstance(entry, DateEntry):
                    entry.set_date(datetime.now())
                else:
                    try: entry.delete(0, "end")
                    except: pass

    def save_pet(self):
        # Clear all images in the temp folder before saving
        temp_dir = "backend/data/temp"
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, f)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass

        required = {
            "pet": [self.name_entry.get(), self.bdate_entry.get()],
            "owner": [self.owner_name_entry.get(), self.owner_phone_entry.get()],
        }
        msgs = {
            "pet": "Pet name and birthdate are required.",
            "owner": "Owner name and contact number are required.",
        }
        for check, fields in required.items():
            if not all(fields):
                messagebox.showwarning("Missing Info", msgs[check])
                return
        try:
            # Validate contact number: must be all digits
            contact_number = required["owner"][1]
            if not contact_number.isdigit():
                messagebox.showerror("Invalid Contact Number", "Contact number must contain only digits (no spaces or letters). Please enter a valid number.")
                return
            pet_controller = PetController()
            # Make image optional
            image_path = self.image_uploader.get_image_path()
            pet_id = pet_controller.add_pet_with_owner(
                Pet(0, required["pet"][0], self.breed_entry.get(), required["pet"][1]),
                Owner(0, required["owner"][0], contact_number, self.owner_address_entry.get()),
                image_path if image_path else None
            )
            controllers = {
                "vet_visits": (VetVisitController, VetVisit),
                "vaccinations": (VaccinationController, Vaccination),
                "feeding_logs": (FeedingLogController, FeedingLog),
                "groomings": (None, None),  # NEW
            }
            for record_type, (ctrl_cls, model_cls) in controllers.items():
                if record_type == "groomings":
                    from backend.controllers.grooming_controller import GroomingLogsController
                    from backend.models.grooming_log import GroomingLog
                    ctrl = GroomingLogsController()
                    for record in self.records[record_type]:
                        model_instance = GroomingLog(
                            id=0,
                            pet_id=pet_id,
                            groom_date="",  # DB will auto-generate
                            groom_type=record["groom_type"],
                            price=record["price"],
                            groomer_name=record["groomer_name"],
                            notes=record["notes"]
                        )
                        ctrl.add_grooming_log(
                            pet_id=pet_id,
                            groom_type=record["groom_type"],
                            groomer_name=record["groomer_name"],
                            notes=record["notes"]
                        )
                else:
                    ctrl = ctrl_cls()
                    for record in self.records[record_type]:
                        model_instance = model_cls(pet_id=pet_id, **record)
                        ctrl.db_handler.insert(model_instance)
            messagebox.showinfo("Saved", f"{required['pet'][0]} and all records added successfully!")
            self.records = {k: [] for k in self.records}
        except Exception as e:
            messagebox.showerror("Error", str(e))

def create_add_pet_view(parent, show_frame):
    AddPetView(parent, show_frame).parent

    copyright_label = get_copyright_label(parent)
    copyright_label.pack(side="bottom", pady=(2, 2))

    return parent