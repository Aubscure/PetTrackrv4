import sqlite3
import os

def export_pets_to_txt(pets, filename="export-import/pets_export.txt"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        for pet in pets:
            f.write(f"Name: {pet['name']}\n")
            f.write(f"Breed: {pet['breed']}\n")
            f.write(f"Age: {pet['age']}\n")
            f.write("-" * 20 + "\n")

def export_pets_to_txt_from_db(
    db_path="backend/data/pets.db",
    output_path="export-import/pets_export.txt"

    
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, breed, birthdate, image_path FROM pets")
    pets = cursor.fetchall()
    conn.close()

    # Write to text file
    with open(output_path, "w", encoding="utf-8") as f:
        for pet in pets:
            f.write(f"ID: {pet[0]}\n")
            f.write(f"Name: {pet[1]}\n")
            f.write(f"Breed: {pet[2]}\n")
            f.write(f"Birthdate: {pet[3]}\n")
            f.write(f"Image Path: {pet[4]}\n")
            f.write("-" * 20 + "\n")
    print(f"Exported pet data to: {output_path}")

# Optional: Run directly for testing
if __name__ == "__main__":
    export_pets_to_txt_from_db()

