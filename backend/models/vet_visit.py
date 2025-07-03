from datetime import datetime

class VetVisit:
    """
    Represents a veterinary visit record for a pet.
    """

    def __init__(self, pet_id: int, visit_date: str, reason: str, notes: str = "", cost: float = 0.0):
        self.pet_id = pet_id
        self.visit_date = visit_date
        self.reason = reason
        self.notes = notes
        self.cost = cost

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "visit_date": self.visit_date,
            "reason": self.reason,
            "notes": self.notes,
            "cost": self.cost
        }

    def __str__(self):
        return f"{self.visit_date} — {self.reason} (₱{self.cost:.2f})"