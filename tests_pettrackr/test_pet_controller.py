import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controllers.pet_controller import PetController
from backend.models.pet import Pet, Owner
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController
from backend.controllers.grooming_controller import GroomingLogsController

class PetTrackrCLI:
    def __init__(self):
        self.controller = PetController()
        self.vet_visit_controller = VetVisitController()
        self.vaccination_controller = VaccinationController()
        self.feeding_log_controller = FeedingLogController()
        self.grooming_controller = GroomingLogsController()
        os.makedirs(os.path.join('..', 'data', 'images'), exist_ok=True)

    def _get_valid_input(self, prompt, validator=None):
        while True:
            try:
                v = input(prompt).strip()
                if validator:
                    validator(v)
                return v
            except ValueError as e:
                print(f"❌ Invalid input: {e}")

    def _validate_date(self, s):
        return datetime.strptime(s, "%Y-%m-%d")

    def add_pet_from_input(self):
        print("\n🐾 Add a New Pet")
        name = self._get_valid_input("Pet Name: ", lambda x: x or ValueError("Name cannot be empty"))
        breed = self._get_valid_input("Breed: ")
        birthdate = self._get_valid_input("Birthdate (YYYY-MM-DD): ", self._validate_date)
        image_path = self._get_valid_input("Path to image file (optional): ").strip() or None

        print("\n👤 Owner Information")
        owner_name = self._get_valid_input("Owner Name: ", lambda x: x or ValueError("Owner name cannot be empty"))
        while True:
            contact_number = self._get_valid_input("Contact Number: ")
            try:
                # Try to validate contact number by creating a temporary Owner
                _ = Owner(id=0, name=owner_name, contact_number=contact_number)
                break
            except ValueError as e:
                print(f"❌ Invalid contact number: {e}")
        address = self._get_valid_input("Address: ")

        pet = Pet(id=0, name=name, breed=breed, birthdate=birthdate, image_path="")
        owner = Owner(id=0, name=owner_name, contact_number=contact_number, address=address)

        if image_path and not os.path.isfile(image_path):
            print("❌ Image not found — saving without image.")
            image_path = None

        try:
            pet_id = self.controller.add_pet_with_owner(pet, owner, image_path)
            print("\n✅ Pet and owner saved successfully!")
            self.view_pet_profile(pet_id)
        except Exception as e:
            print(f"❌ Error saving pet: {e}")

    def list_pets(self, pets=None, owners=None, title="📋 All Pets with Owners"):
        if pets is None or owners is None:
            pets, owners = self.controller.get_pets_with_owners()

        print(f"\n{title}:")
        try:
            if not pets:
                print("No pets found in database")
                return

            for i, (pet, owner) in enumerate(zip(pets, owners), 1):
                print(f"\n{i}. {pet}\n   Owner: {owner if owner else 'No owner information'}")

            while True:
                choice = input("\nEnter pet number to view profile (or 'back' to return): ").strip().lower()
                if choice == 'back':
                    return

                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pets):
                        self.view_pet_profile(pets[idx].id)
                        return
                    print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving pets: {e}")

    def _add_vet_visit(self, pet_id):
        print("\n🩺 Add Vet Visit")

        VET_VISIT_REASONS = {
            "1": "Checkup",
            "2": "Vaccination",
            "3": "Dental Cleaning",
            "4": "Injury Treatment",
            "5": "Surgery",
            "6": "Skin Problem",
            "7": "Eye/Ear Issue",
            "8": "Digestive Issue",
            "9": "Post-Op Follow-up",
            "10": "Other"
        }

        print("\nPredefined Vet Visit Reasons:")
        for key, reason in VET_VISIT_REASONS.items():
            print(f"{key}. {reason}")

        reason_choice = input("\nChoose reason (1-10): ").strip()
        reason = VET_VISIT_REASONS.get(reason_choice, "Other")

        visit_date = datetime.today().strftime("%Y-%m-%d")

        cost = float(self._get_valid_input("Cost: ", lambda x: float(x)))

        from backend.models.vet_visit import VetVisit
        vet_visit = VetVisit(
            pet_id=pet_id,
            visit_date=visit_date,
            reason=reason,
            notes=input("Notes (optional): "),
            cost=cost
        )

        data = vet_visit.to_dict()
        self.vet_visit_controller.create(data)
        print("✅ Vet Visit saved.")

    def _add_vaccination(self, pet_id):
        print("\n💉 Add Vaccination")

        predefined_vaccines = {
            "1": ("Rabies", 400),
            "2": ("Distemper", 350),
            "3": ("Bordetella", 300),
            "4": ("Parvo", 350)
        }

        print("\nPredefined Vaccines:")
        for key, (vaccine, price) in predefined_vaccines.items():
            print(f"{key}. {vaccine} (Price: ₱{price})")

        vaccine_choice = input("\nChoose vaccine (1-4): ").strip()
        vaccine_name, price = predefined_vaccines.get(vaccine_choice, ("Rabies", 400))

        date_administered = self._get_valid_input("Date Administered (YYYY-MM-DD): ", self._validate_date)

        from backend.models.vaccination import Vaccination
        vax = Vaccination(
            pet_id=pet_id,
            vaccine_name=vaccine_name,
            date_administered=date_administered,
            price=price,
            notes=input("Notes (optional): ")
        )

        data = vax.to_dict()
        data.pop("is_due", None)

        self.vaccination_controller.create(data)
        print("✅ Vaccination saved.")

    def _add_feeding_log(self, pet_id):
        print("\n🍖 Add Feeding Log")
        data = {
            "pet_id": pet_id,
            "start_date": self._get_valid_input("Start Date (YYYY-MM-DD): ", self._validate_date),
            "num_days": int(self._get_valid_input("Number of Days: ", lambda x: int(x))),
            "feed_once": input("Feed Once Daily? (y/n): ").lower() == 'y',
            "feed_twice": input("Feed Twice Daily? (y/n): ").lower() == 'y',
            "feed_thrice": input("Feed Thrice Daily? (y/n): ").lower() == 'y'
        }
        self.feeding_log_controller.create(data)
        print("✅ Feeding Log saved.")

    def _add_grooming_log(self, pet_id):
        print("\n✂️ Add Grooming Log")
        groom_types = {
            '1': ('basic', 500),
            '2': ('full', 800),
            '3': ('premium', 1200)
        }

        print("\nGrooming Types:")
        for key, (name, price) in groom_types.items():
            print(f"{key}. {name.capitalize()} (₱{price})")

        groom_choice = input("\nChoose grooming type (1-3): ").strip()
        if groom_choice not in groom_types:
            print("❌ Invalid choice, using basic grooming")
            groom_choice = '1'

        groom_type, price = groom_types[groom_choice]
        groomer_name = input("Groomer Name: ")
        notes = input("Notes (optional): ")

        inserted_id = self.grooming_controller.add_grooming_log(
            pet_id=pet_id,
            groom_type=groom_type,
            groomer_name=groomer_name,
            notes=notes,
            price=price
        )
        print(f"✅ Grooming Log saved with ID: {inserted_id}")


    def view_pet_profile(self, pet_id):
        try:
            pet, owner = self.controller.get_pet_by_id(pet_id)
            if not pet:
                print(f"❌ Pet with ID {pet_id} not found")
                return

            while True:
                print("\n" + "="*40 + f"\n🐾 {pet.name}'s Profile\n" + "="*40)
                print(f"Breed: {pet.breed}\nBirthdate: {pet.birthdate}")

                if pet.image_path and os.path.exists(os.path.join(self.controller.data_dir, pet.image_path)):
                    print(f"Image: {pet.image_path}")

                if owner:
                    print(f"\n👤 Owner Information:\nName: {owner.name}\nContact: {owner.contact_number}\nAddress: {owner.address}")

                for label, ctrl, attr, fmt in [
                    ("🩺 Vet Visits", self.vet_visit_controller, "get_by_pet_id", lambda v: f" - {v.visit_date}: {v.reason}" + (f"\n   Notes: {v.notes}" if v.notes else "")),
                    ("💉 Vaccinations", self.vaccination_controller, "get_by_pet_id", None),
                    ("🍖 Feeding Logs", self.feeding_log_controller, "get_by_pet_id", None),
                    ("✂️ Grooming Logs", self.grooming_controller, "get_grooming_logs_for_pet", None),
                ]:
                    try:
                        items = getattr(ctrl, attr)(pet_id)
                        if items:
                            print(f"\n{label}:")
                            if label == "💉 Vaccinations":
                                for v in items:
                                    print(f" - {v.vaccine_name} (Administered: {v.date_administered}, Next Due: {v.next_due})")
                                    if hasattr(v, 'notes') and v.notes:
                                        print(f"   Notes: {v.notes}")
                            elif label == "🍖 Feeding Logs":
                                base = 350
                                total = 0
                                print(" --- Feeding Log Receipt ---")
                                for v in items:
                                    plan = ", ".join([desc for desc, flag in [("Once", v.feed_once), ("Twice", v.feed_twice), ("Thrice", v.feed_thrice)] if flag]) or "No feeding"
                                    addon = 85 if v.feed_once else 170 if v.feed_twice else 255 if v.feed_thrice else 0
                                    fee = v.num_days * (base + addon)
                                    total += fee
                                    print(f" - {v.start_date} | {v.num_days} day(s) | Plan: {plan}")
                                    print(f"  Breakdown: {v.num_days} x (₱{base} base + ₱{addon} feeding) = ₱{fee}")
                                print(" --------------------------")
                                print(f" TOTAL FEEDING INVOICE: ₱{total}")
                            elif label == "✂️ Grooming Logs":
                                for v in items:
                                    print(f" - {v.groom_type.capitalize()} grooming by {v.groomer_name}")
                                    print(f"   Date: {v.groom_date}")
                                    print(f"   Price: ₱{v.price:,.2f}")
                                    if hasattr(v, 'notes') and v.notes:
                                        print(f"   Notes: {v.notes}")
                            else:
                                [print(fmt(v)) for v in items]
                    except Exception as e:
                        print(f"\n⚠️ Could not load {label.lower()}: {str(e)}")

                print("\nOptions:\n1. Add Vet Visit\n2. Add Vaccination\n3. Add Feeding Log\n4. Add Grooming Log\n5. Back to Menu")
                choice = input("\nChoose an option: ").strip()
                if choice == "1":
                    self._add_vet_visit(pet.id)
                elif choice == "2":
                    self._add_vaccination(pet.id)
                elif choice == "3":
                    self._add_feeding_log(pet.id)
                elif choice == "4":
                    self._add_grooming_log(pet.id)
                elif choice == "5":
                    return
                else:
                    print("❌ Invalid choice. Please try again.")
        except Exception as e:
            print(f"❌ Error accessing pet profile: {e}")

    def vaccination_and_visits_menu(self):
        print("\n💉 Vaccination and Visits Menu")
        try:
            pets, owners = self.controller.get_pets_with_vacc_or_vet_records()
            if not pets:
                print("No pets with vaccination or vet visit records found")
                return

            print("\nPets with Vaccination or Vet Visit Records:")
            for i, (pet, owner) in enumerate(zip(pets, owners), 1):
                vaccs = self.vaccination_controller.get_by_pet_id(pet.id)
                visits = self.vet_visit_controller.get_by_pet_id(pet.id)
                print(f"\n{i}. {pet.name} (ID: {pet.id})")
                print(f" Breed: {pet.breed}")
                print(f" Owner: {owner.name if owner else 'No owner'}")
                print(f" Vaccinations: {len(vaccs)}")
                print(f" Vet Visits: {len(visits)}")

            while True:
                choice = input("\nEnter pet number to view details (or 'back' to return): ").strip().lower()
                if choice == 'back':
                    return
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pets):
                        self.view_pet_profile(pets[idx].id)
                        return
                    print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving records: {e}")

    def daycare_menu(self):
        print("\n🏠 Daycare Menu")
        try:
            pets, owners = self.controller.get_pets_with_feeding_logs()
            if not pets:
                print("No pets with feeding logs found")
                return

            print("\nPets with Daycare/Feeding Records:")
            for i, (pet, owner) in enumerate(zip(pets, owners), 1):
                logs = self.feeding_log_controller.get_by_pet_id(pet.id)
                print(f"\n{i}. {pet.name} (ID: {pet.id})")
                print(f" Breed: {pet.breed}")
                print(f" Owner: {owner.name if owner else 'No owner'}")
                print(f" Feeding Logs: {len(logs)}")

            while True:
                choice = input("\nEnter pet number to view details (or 'back' to return): ").strip().lower()
                if choice == 'back':
                    return
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pets):
                        self.view_pet_profile(pets[idx].id)
                        return
                    print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving records: {e}")

    def grooming_menu(self):
        print("\n✂️ Grooming Menu")
        try:
            pets = []
            all_pets, _ = self.controller.get_pets_with_owners()
            for pet in all_pets:
                logs = self.grooming_controller.get_grooming_logs_for_pet(pet.id)
                if logs:
                    pets.append(pet)

            if not pets:
                print("No pets with grooming logs found")
                return

            print("\nPets with Grooming Records:")
            for i, pet in enumerate(pets, 1):
                logs = self.grooming_controller.get_grooming_logs_for_pet(pet.id)
                owner = self.controller.get_pet_by_id(pet.id)[1]
                print(f"\n{i}. {pet.name} (ID: {pet.id})")
                print(f" Breed: {pet.breed}")
                print(f" Owner: {owner.name if owner else 'No owner'}")
                print(f" Grooming Logs: {len(logs)}")

            while True:
                choice = input("\nEnter pet number to view details (or 'back' to return): ").strip().lower()
                if choice == 'back':
                    return
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pets):
                        self.view_pet_profile(pets[idx].id)
                        return
                    print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving records: {e}")

    def run(self):
        menu = {
            "1": ("Add Pet", self.add_pet_from_input),
            "2": ("View Pets", self.list_pets),
            "3": ("Vaccination and Visits", self.vaccination_and_visits_menu),
            "4": ("Daycare", self.daycare_menu),
            "5": ("Grooming", self.grooming_menu),
            "6": ("Exit", lambda: exit(print("Goodbye!")))
        }

        while True:
            print("\n=== PetTrackr Main Menu ===")
            for key, (label, _) in menu.items():
                print(f"{key}. {label}")

            choice = input("\nChoose an option: ").strip()
            if choice in menu:
                menu[choice][1]()
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        PetTrackrCLI().run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
