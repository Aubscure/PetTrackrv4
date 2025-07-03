import customtkinter as ctk
from frontend.components.pet_card_with_records import PetCardWithRecords
from backend.controllers.pet_controller import PetController

def main():
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Pet Card With Records Demo")

    # Fetch a pet and owner for demo
    pet_ctrl = PetController()
    pets, owners = pet_ctrl.get_pets_with_vacc_or_vet_records()
    image_store = []

    # Show the first pet with records
    if pets:
        card = PetCardWithRecords(root, pets[0], image_store, owner=owners[0])
        card.pack(padx=20, pady=20)
    else:
        ctk.CTkLabel(root, text="No pets with records found.").pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()