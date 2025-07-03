# grooming_log.py
# File: backend/models/grooming_log.py
from datetime import datetime

class GroomingLog:
    """
    Represents a grooming log entry for a pet.
    """

    def __init__(self, id: int, pet_id: int, groom_date: str, groom_type: str,
                 price: float, groomer_name: str, notes: str = ""):
        self.id = id
        self.pet_id = pet_id
        self.groom_date = groom_date
        self.groom_type = groom_type
        self.price = price
        self.groomer_name = groomer_name
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "groom_date": self.groom_date,
            "groom_type": self.groom_type,
            "price": self.price,
            "groomer_name": self.groomer_name,
            "notes": self.notes
        }

    def __str__(self):
        return f"{self.groom_date} — {self.groom_type.capitalize()} Groom by {self.groomer_name} for ₱{self.price:,.2f}"