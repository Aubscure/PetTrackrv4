# PetTrackr: Programming Structures Overview

## This document explains how core programming structures and concepts are implemented in the PetTrackr project. Each section includes specific examples and file references so you can easily locate them in the codebase.

## 1. Sequential Structures

**Definition:** Code that executes line by line, in order.
Explanation: Imagine you're following a recipe. You do step 1, then step 2, then step 3, and so on. In programming, sequential structures work the same way. The code executes one line after another.

- **Example:** The setup and initialization code in `backend/data/pets_db.py` and `frontend/gui.py` runs sequentially.
- **Code Reference:**
  backend/data/vaccinations_db.py
  with sqlite3.connect(self.db_path) as conn: #Explanation: This line connects to a database. Think of it like opening a file cabinet where you keep all your important papers. sqlite3.connect(self.db_path) is the command to open the cabinet, and as conn means we're giving it a nickname "conn" so we can refer to it easily.
  cursor = conn.cursor()
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS vaccinations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pet_id INTEGER NOT NULL,
  vaccine_name TEXT,
  date_administered TEXT,
  next_due TEXT,
  price INTEGER,
  notes TEXT,
  FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
  )
  ''')
  conn.commit()

## Explanation: This code connects to a database and creates a table for vaccinations if it doesn't already exist. It runs line by line, just like following a recipe.

## 2. Decision Structures

**Definition:** Code that makes choices using `if`, `elif`, and `else`.
Explanation: Think of it like making decisions in everyday life. If it's raining, you bring an umbrella. If not, you don't. In programming, decision structures help the code make choices.

- **Example:** Input validation and error handling in `frontend/views/pet_form_view.py` and `backend/services/data_import.py`.
- **Code Reference:**
  - `frontend/views/pet_form_view.py`
    if not pet_name:
    messagebox.showerror("Error", "Pet name is required.")
    return
    elif not age.isdigit():
    messagebox.showerror("Error", "Age must be a number.")
    return

Explanation: This code checks if the pet name is provided and if the age is a number. If not, it shows an error message. It's like checking if you have all the ingredients before you start cooking.

---

## 3. Repetition Structures

**Definition:** Code that repeats actions using `for` or `while` loops.
Explanation: Imagine you're washing dishes. You wash one dish, then another, and another, until all the dishes are clean. In programming, repetition structures let you repeat actions.

- **Example:** Iterating over pets for import/export in `backend/services/data_export.py` and `backend/services/data_import.py`.
- **Code Reference:**
  - `backend/services/data_export.py`
    for pet in pets:
    file.write(f"{pet['name']},{pet['age']},{pet['type']}\n")

Explanation: This code goes through a list of pets and writes their information to a file. It's like washing each dish one by one.

---

## 4. String Methods

**Definition:** Built-in methods for manipulating strings.
Explanation: Strings are just text. String methods are like tools that help you change or use that text in different ways.

- **Example:** Parsing and formatting data in `backend/services/data_import.py`.
- **Code Reference:**
  - `backend/services/data_import.py`
    fields = line.strip().split(',')
    name = fields[0].capitalize()

Explanation: This code takes a line of text, removes extra spaces, splits it into parts, and makes the first letter of the name capital. It's like editing a sentence to make it look nice.

---

## 5. Text File Manipulation

**Definition:** Reading from and writing to text files.
Explanation: Think of a text file like a notebook. You can write things in it and read things from it. In programming, you can do the same with text files.

- **Example:** Exporting and importing pet data in `backend/services/data_export.py` and `backend/services/data_import.py`.
- **Code Reference:**
  - `backend/services/data_export.py`
    with open(filepath, 'w') as file:
    for pet in pets:
    file.write(f"{pet['name']},{pet['age']},{pet['type']}\n")
    Explanation: This code opens a file and writes the information of each pet into it. It's like writing a list of pets in a notebook.

---

## 6. Lists and Dictionaries

**Definition:** Data structures for storing collections and key-value pairs.
Explanation: A list is like a shopping list. It has items in order. A dictionary is like a phone book. It has names and corresponding phone numbers.

- **Example:** Lists for storing pets, dictionaries for pet attributes.
- **Code Reference:**
  - `backend/services/data_export.py`
    pets = [
    {"name": "Buddy", "age": 3, "type": "Dog"},
    {"name": "Mittens", "age": 2, "type": "Cat"}
    ]
    Explanation: This code creates a list of pets, where each pet is a dictionary with a name, age, and type. It's like having a list of pets with their details.

---

## 7. Functions

**Definition:** Reusable blocks of code.
Explanation: Think of a function like a recipe. You can use the same recipe to make a cake many times. In programming, functions let you reuse code.

- **Example:** Utility and handler functions throughout the codebase.
- **Code Reference:**
  - `backend/services/data_export.py`
    def export_pets_to_txt_from_db(filepath): # function body
    Explanation: This code defines a function that exports pet data to a text file. You can call this function whenever you need to export the data.

---

## 8. Program Modularization

**Definition:** Organizing code into modules and packages.
Explanation: Imagine you have a big toy box. You can organize your toys into smaller boxes, like one for cars, one for dolls, and one for blocks. In programming, modularization helps you organize your code into smaller, manageable parts.

- **Example:**
  - `frontend/` for GUI
  - `backend/` for logic, models, controllers, services
  - `tests_pettrackr/` for tests

---

## 9. Simple Graphics and Image Processing

**Definition:** Loading, displaying, and manipulating images.
Explanation: Think of it like editing photos on your phone. You can rotate, crop, and change the colors. In programming, you can do similar things with images.

- **Example:** Image upload and manipulation in `frontend/components/image_uploader.py` using PIL.
- **Code Reference:**
  - `frontend/components/image_uploader.py`
    from PIL import Image
    img = Image.open(filepath)
    img = img.rotate(90)
    img.save(new_filepath)

Explanation: This code opens an image, rotates it by 90 degrees, and saves it. It's like editing a photo to make it look better.

---

## 10. Graphical User Interfaces

**Definition:** Visual interfaces for user interaction.
A graphical user interface (GUI) is like the screen on your phone. You can tap buttons and see pictures. In programming, a GUI lets users interact with the program visually.

- **Example:** Built with customtkinter in `frontend/gui.py` and views in `frontend/views/`.
- **Code Reference:**
  - `frontend/gui.py`
    import customtkinter as ctk
    class App(ctk.CTk):
    def **init**(self):
    super().**init**() # setup GUI

Explanation: This code sets up the main window of the PetTrackr application. It's like designing the screen of a phone app.

---

## 11. Designing with Classes

**Definition:** Object-oriented programming using classes.
Explanation: Think of a class like a blueprint for a house. You can use the same blueprint to build many houses. In programming, classes let you create objects with similar properties and behaviors.

- **Example:** Models, controllers, and GUI components.
- **Code Reference:**
  - `backend/models/pet.py`
    class Pet:
    def **init**(self, name, age, pet_type):
    self.name = name
    self.age = age
    self.pet_type = pet_type

Explanation: This code defines a class for a pet. Each pet has a name, age, and type. It's like having a blueprint for creating pets.

---

## 12. Network Application and Client/Server Programming

**Definition:** Communication over a network.
**Where in PetTrackr:**

- **Status:** Not implemented.

---

## 13. Searching, Sorting, and Complexity

**Definition:** Algorithms for finding and ordering data; analyzing efficiency.
Explanation: Imagine you have a big box of toys. Searching is like looking for a specific toy in that box. Sorting is like arranging your toys in order, maybe by size or color. Complexity is about how long it takes to find or sort your toys.

- **Example:**
  def search_pets_by_name(self, name):
  query = "SELECT \* FROM pets WHERE name LIKE ?"
  self.cursor.execute(query, (f"%{name}%",))
  return self.cursor.fetchall()

Explanation: This code searches for pets by their name in a database. It's like looking for a book with a specific title in a library. The LIKE keyword helps find names that match a pattern, and % is a wildcard that matches any sequence of characters.

---

## Summary Table

| Structure                          | Present? | Example File(s) / Location(s)                |
| ---------------------------------- | -------- | -------------------------------------------- |
| Sequential Structures              | Yes      | `backend/data/pets_db.py`, `frontend/gui.py` |
| Decision Structures                | Yes      | `frontend/views/pet_form_view.py`            |
| Repetition Structures              | Yes      | `backend/services/data_export.py`            |
| String Methods                     | Yes      | `backend/services/data_import.py`            |
| Text File Manipulation             | Yes      | `backend/services/data_export.py`            |
| Lists and Dictionaries             | Yes      | `backend/services/data_export.py`            |
| Functions                          | Yes      | Throughout                                   |
| Program Modularization             | Yes      | Project structure                            |
| Simple Graphics & Image Processing | Yes      | `frontend/components/image_uploader.py`      |
| Graphical User Interfaces          | Yes      | `frontend/gui.py`                            |
| Designing with Classes             | Yes      | `backend/models/pet.py`                      |
| Network Application/Client-Server  | No       | Placeholder only                             |
| Searching, Sorting, Complexity     | Partial  | SQL queries                                  |

---

PSEUDOCODE
def displayPetDetails(petName, petBreed, petAge, petImage, ownerName, ownerContact, ownerAddress, index, vaccinations):
print("Name: " + petName[index], end='', flush=True)
print("Breed: " + petBreed[index])
print("Age: " + str(petAge[index]))
print("Image: " + petImage[index])
print("Owner's name: " + ownerName[index])
print("Owner's contact: " + ownerContact[index])
print("Owner's address: " + ownerAddress[index])
print("Vaccinations: " + vaccinations[index])

def petWithVaccinationsAndVisits(petName, petBreed, petAge, petImage, ownerName, ownerContact, ownerAddress, index, vaccinations):
index = 1
petNum = 1

    for i in range(0, petNum - 1 + 1, 1):
        if vaccinations[index] == "none":
            print("No pets with Vaccinations and Vet visits")
        else:
            print("Name:          " + petName[index], end='', flush=True)
            print("Breed:          " + petBreed[index])
            print("Age:          " + str(petAge[index]))
            print("Image:          " + petImage[index])
            print("Owner's name:          " + ownerName[index])
            print("Owner's contact:          " + ownerContact[index])
            print("Owner's address:          " + ownerAddress[index])
            print("Vaccinations: " + vaccinations[index])

def savePetDetails(petName, petBreed, petAge, petImage, ownerName, ownerContact, ownerAddress, index, vaccinations):
print("Enter pet Name")
petName[index] = input()
print("Enter pet breed")
petBreed[index] = input()
print("Enter pet Age")
petAge[index] = int(input())
print("Enter pet image or none")
petImage[index] = input()
print("Enter pet owner's name")
ownerName[index] = input()
print("Enter pet owner's contact number")
ownerContact[index] = input()
print("Enter pet owner's address")
ownerAddress[index] = input()

    vaccService = 1
    print("Want to add Vaccine to your pet?")
    serviceUserInput = input()

    if serviceUserInput == "yes":
        for i in range(0, vaccService - 1 + 1, 1):
            print("Choose what vaccination you want" + chr(13) + "1. Rabies     200" + chr(13) + "2. Distemper     250")
            vaccinationInput = int(input())
            if vaccinationInput == 1:
                vaccinations[index] = "Rabies 200"
            else:
                if vaccinationInput == 2:
                    vaccinations[index] = "Distemper 250"
                else:
                    vaccinations[index] = "none"
    else:
        vaccinations[index] = "None"

petName = [""] _ (10)
petBreed = [""] _ (10)
petImage = [""] _ (10)
ownerName = [""] _ (10)
ownerAddress = [""] _ (10)
ownerContact = [""] _ (10)
vaccinations = [""] _ (10)
petAge = [0] _ (10)

dashboard = True

addPets = 1
viewAllPets = 2
vaccinationAndVisits = 3
feedingLogs = 4
groomingLogs = 5
exit = 9
index = 1

while dashboard == True:
print("Choose what number you want." + chr(13) + "1. Add pets | 2. View all pets | 3. View pets with vaccinations and visits | 4. View pets with feeding logs | 5. View pets with grooming logs | 9. Exit")
userInput = int(input())

    if userInput == 1:
        numPets = 1
        for i in range(0, numPets - 1 + 1, 1):
            savePetDetails(petName, petBreed, petAge, petImage, ownerName, ownerContact, ownerAddress, index, vaccinations)
    else:
        if userInput == 2:
            displayPetDetails(petName, petBreed, petAge, petImage, ownerName, ownerContact, ownerAddress, index, vaccinations)
        else:
            if userInput == 3:
                petWithVaccinationsAndVisits(petName, petBreed, petAge, petImage, ownerName, ownerContact, ownerAddress, index, vaccinations)
            else:
                if userInput == 9:
                    print("Bye! See you again, soon!")
                    dashboard = False
