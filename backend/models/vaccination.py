from datetime import datetime, timedelta

class Vaccination:
    """Represents a vaccination record for a pet."""

    DEFAULT_INTERVALS = {
        "Rabies": 365,
        "Distemper": 365,
        "Bordetella": 180,
        "Parvo": 365
    }

    VACCINE_PRICES = {
        "Rabies": 400,
        "Distemper": 350,
        "Bordetella": 300,
        "Parvo": 350
    }

    def __init__(self, pet_id: int, vaccine_name: str, date_administered: str,
                 next_due: str = "", price: int = 0, notes: str = ""):
        self.pet_id = pet_id
        self.vaccine_name = vaccine_name
        self.date_administered = date_administered
        self.next_due = next_due or self.auto_calculate_next_due()
        self.price = price or self.VACCINE_PRICES.get(vaccine_name, 0)
        self.notes = notes

    def auto_calculate_next_due(self) -> str:
        """Sets default `next_due` based on known intervals."""
        try:
            days = self.DEFAULT_INTERVALS.get(self.vaccine_name, 365)  # Default to yearly
            base_date = datetime.strptime(self.date_administered, "%Y-%m-%d")
            return (base_date + timedelta(days=days)).strftime("%Y-%m-%d")
        except ValueError:
            return ""

    def is_due(self) -> bool:
        try:
            due = datetime.strptime(self.next_due, '%Y-%m-%d')
            return datetime.today().date() >= due.date()
        except ValueError:
            return False

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "vaccine_name": self.vaccine_name,
            "date_administered": self.date_administered,
            "next_due": self.next_due,
            "price": self.price,
            "notes": self.notes,
            "is_due": self.is_due()
        }

    def __str__(self):
        status = "✔️ Up to date" if not self.is_due() else "⚠️ Due"
        return f"{self.vaccine_name} (Next due: {self.next_due}, Price: ₱{self.price}) → {status}"