## File: backend/controllers/grooming_controller.py
import sqlite3
import os
from backend.models.grooming_log import GroomingLog  # Adjust path as needed
from typing import Optional

class GroomingLogsController:
    """
    Controller for managing grooming log database interactions.
    """

    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'grooming_logs.db')

    def add_grooming_log(self, pet_id: int, groom_type: str, groomer_name: str, notes: str = "", price: float = 0.0) -> Optional[int]:
        """
        Inserts a new grooming log into the database. Date is auto-generated. Price is based on grooming type.
        """
        PRICE_MAP = {
            'basic': 1000.0,
            'custom': 1500.0,
            'premium': 1800.0
        }

        price = PRICE_MAP.get(groom_type, 0.0)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO grooming_logs (pet_id, groom_type, price, groomer_name, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (pet_id, groom_type, price, groomer_name, notes))
            conn.commit()
            return cursor.lastrowid


    def get_grooming_logs_for_pet(self, pet_id: int):
        """
        Retrieves all grooming logs for a given pet.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, pet_id, groom_date, groom_type, price, groomer_name, notes
                FROM grooming_logs
                WHERE pet_id = ?
                ORDER BY groom_date DESC
            ''', (pet_id,))
            rows = cursor.fetchall()

        return [GroomingLog(*row) for row in rows]