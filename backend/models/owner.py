class Owner:
    """
    Represents a pet owner with contact details.
    """

    def __init__(self, id: int, name: str, contact_number: int = None, address: str = None):
        """
        Initializes an Owner instance.

        Args:
            id (int): The unique owner ID from the database.
            name (str): The owner's full name.
            contact_number (str, optional): The owner's phone number.
            address (str, optional): The owner's address.
        """
        self.id = id
        self.name = name
        self.contact_number = contact_number
        self.address = address

    def to_dict(self):
        """
        Returns a dictionary representation of the owner.
        """
        return {
            "id": self.id,
            "name": self.name,
            "contact_number": self.contact_number,
            "address": self.address
        }

    def __str__(self):
        """
        Returns a readable string summary of the owner.
        """
        contact_info = f"📞 {self.contact_number}" if self.contact_number else "📞 N/A"
        location = f"🏠 {self.address}" if self.address else "🏠 N/A"
        return f"{self.name} — {contact_info}, {location}"