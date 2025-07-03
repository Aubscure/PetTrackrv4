# filepath: d:\codes\Giedel\Python-GUI\PetTrackr\tests_pettrackr\test_get_both_records.py(for pets with vaccination OR vet visit records)

from backend.controllers.pet_controller import PetController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.vet_visit_controller import VetVisitController

def debug_print_pet(pet, owner, vaccs, visits):
    print(f"Pet: {pet.name} (ID: {pet.id})")
    print(f"  Breed: {pet.breed}")
    print(f"  Birthdate: {pet.birthdate}")
    if owner:
        print(f"  Owner: {owner.name} ({owner.contact_number})")
    else:
        print("  Owner: None")
    print(f"  Vaccinations: {len(vaccs)}")
    for v in vaccs:
        print(f"    - {v}")
    print(f"  Vet Visits: {len(visits)}")
    for v in visits:
        print(f"    - {v}")
    print("-" * 40)

def main():
    pet_ctrl = PetController()
    vax_ctrl = VaccinationController()
    visit_ctrl = VetVisitController()

    pets, owners = pet_ctrl.get_pets_with_vacc_or_vet_records()
    print(f"Found {len(pets)} pets with vaccination OR vet visit records.\n")

    for pet, owner in zip(pets, owners):
        vaccs = vax_ctrl.get_by_pet_id(pet.id)
        visits = visit_ctrl.get_by_pet_id(pet.id)
        debug_print_pet(pet, owner, vaccs, visits)

if __name__ == "__main__":
    main()

# To run this test module, use the following command:
# python -m tests_pettrackr.test_get_both_records