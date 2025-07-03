from datetime import datetime
from typing import Optional, Union
import re

class Pet:
    """Represents a pet with identifying information and helper methods."""

    def __init__(
        self,
        id: int,
        name: str,
        breed: str,
        birthdate: str,
        image_path: Optional[str] = None,
        owner_id: Optional[int] = None  # Explicit link to owner
    ):
        """
        Args:
            id: Unique pet ID (database primary key).
            name: Pet's name (auto-trimmed).
            breed: Pet's breed (auto-trimmed, optional).
            birthdate: Format YYYY-MM-DD (validated in age()).
            image_path: Optional path to pet photo (auto-trimmed).
            owner_id: Foreign key linking to Owner (optional but recommended).
        """
        self.id = id
        self.name = name.strip()
        self.breed = breed.strip() if breed else None
        self.birthdate = birthdate
        self.image_path = image_path.strip() if image_path else None
        self.owner_id = owner_id  # Critical for database relationships

    def age(self) -> Union[int, str]:
        """Calculates age in years or 'Unknown' if invalid date."""
        try:
            birth = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
            age = (datetime.now().date() - birth).days // 365
            return max(0, age)
        except (ValueError, TypeError):
            return "Unknown"

    def to_dict(self) -> dict:
        """Serializes pet data for storage/API with computed age."""
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "birthdate": self.birthdate,
            "age": self.age(),  # Computed property
            "image_path": self.image_path,
            "owner_id": self.owner_id  # Maintain relational integrity
        }

    def __str__(self) -> str:
        """Display-friendly format: 'Name (Breed) | Age: X'."""
        return f"{self.name} ({self.breed or 'Unknown breed'}) | Age: {self.age()}"


class Owner:
    """Represents a pet owner with validated contact information."""

    def __init__(
        self,
        id: int,
        name: str,
        contact_number: Optional[str] = None,
        address: Optional[str] = None
    ):
        """
        Args:
            id: Unique owner ID (database primary key).
            name: Owner's full name (auto-trimmed).
            contact_number: Digits-only phone (auto-cleaned).
            address: Physical address (auto-trimmed).
        """
        self.id = id
        self.name = name.strip()
        if contact_number is not None:
            if isinstance(contact_number, int):
                contact_number = str(contact_number)
            elif not isinstance(contact_number, str):
                raise ValueError("Contact number must be an integer or a string of digits.")
            if not contact_number.isdigit():
                raise ValueError("Contact number must contain only digits.")
            self.contact_number = self._clean_phone(contact_number)
        else:
            self.contact_number = None
        self.address = address.strip() if address else None

    @staticmethod
    def _clean_phone(phone: str) -> Optional[str]:
        """Extracts digits only or returns None if invalid."""
        digits = re.sub(r"[^\d]", "", phone)
        return digits if 7 <= len(digits) <= 15 else None  # Global phone standards

    def to_dict(self) -> dict:
        """Serializes owner data for storage/API."""
        return {
            "id": self.id,
            "name": self.name,
            "contact_number": self.contact_number,
            "address": self.address
        }

    def __str__(self) -> str:
        """Display-friendly format: 'Name | 📞 Phone | 🏠 Address'."""
        return " | ".join(filter(None, [
            self.name,
            f"📞 {self.contact_number}" if self.contact_number else None,
            f"🏠 {self.address}" if self.address else None
        ]))