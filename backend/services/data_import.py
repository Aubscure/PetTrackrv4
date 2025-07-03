def import_pets_from_txt(filename="export-import/pets_export.txt"):
    pets = []
    with open(filename, "r", encoding="utf-8") as f:
        pet = {}
        for line in f:
            if line.startswith("ID:"):
                pet["id"] = line.split(":", 1)[1].strip()
            elif line.startswith("Name:"):
                pet["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("Breed:"):
                pet["breed"] = line.split(":", 1)[1].strip()
            elif line.startswith("Birthdate:"):
                pet["birthdate"] = line.split(":", 1)[1].strip()
            elif line.startswith("Image Path:"):
                pet["image_path"] = line.split(":", 1)[1].strip()
            elif line.strip() == "-" * 20:
                if pet:
                    pets.append(pet)
                    pet = {}
    return pets