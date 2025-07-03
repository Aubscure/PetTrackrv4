# filepath: d:\codes\Giedel\Python-GUI\PetTrackr\tests_pettrackr\test_grooming_logs_controller.py(for pets with grooming logs)
from backend.controllers.grooming_controller import GroomingLogsController

def test_grooming_logs():
    controller = GroomingLogsController()

    # Step 1: Insert a grooming log
    inserted_id = controller.add_grooming_log(
        pet_id=1,  # Use a valid pet_id existing in your pets table
        groom_type='premium',
        groomer_name='Ava',
        notes='Deep clean, trimmed tail ✂️'
    )
    print(f"✅ Inserted grooming log with ID: {inserted_id}")

    # Step 2: Fetch grooming logs for that pet
    logs = controller.get_grooming_logs_for_pet(pet_id=1)
    for log in logs:
        print(log)
        print(f"Price: ₱{log.price:,.2f}")  # <-- Explicitly print the price

if __name__ == "__main__":
    test_grooming_logs()