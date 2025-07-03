# filepath: d:\codes\Giedel\Python-GUI\PetTrackr\tests_pettrackr\test_get_both_records.py(for pets with feeding logs)
from backend.controllers.pet_controller import PetController
from backend.controllers.feeding_log_controller import FeedingLogController

if __name__ == "__main__":
    controller = PetController()
    feeding_ctrl = FeedingLogController()
    pets, owners = controller.get_pets_with_feeding_logs()
    print("Pets with feeding logs:")
    for pet, owner in zip(pets, owners):
        print(f"Pet: {pet.name} (ID: {pet.id}) | Owner: {owner.name if owner else 'No owner'}")
        logs = feeding_ctrl.get_by_pet_id(pet.id)
        if logs:
            for log in logs:
                print(f"  - {log}")
        else:
            print("  No feeding logs found.")