# File: backend/database/vaccinations_db_handler.py
import sqlite3
import os
from backend.models.vaccination import Vaccination

class VaccinationDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', 'data', 'vaccinations.db')

    def connect(self):
        return sqlite3.connect(self.db_path)

    def insert(self, vax: Vaccination):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO vaccinations (pet_id, vaccine_name, date_administered, next_due, price, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (vax.pet_id, vax.vaccine_name, vax.date_administered, vax.next_due, vax.price, vax.notes)
            )
            conn.commit()
            return cursor.lastrowid

    def update(self, vax: Vaccination):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE vaccinations
                SET pet_id = ?, vaccine_name = ?, date_administered = ?, next_due = ?, price = ?, notes = ?
                WHERE id = ?
                """,
                (vax.pet_id, vax.vaccine_name, vax.date_administered, vax.next_due, vax.price, vax.notes)
            )
            conn.commit()

    def get_by_pet_id(self, pet_id: int) -> list[Vaccination]:
        """Get all vaccinations for a specific pet ID"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pet_id, vaccine_name, date_administered, next_due, price, notes
                FROM vaccinations
                WHERE pet_id = ?
                ORDER BY date_administered DESC
            """, (pet_id,))
            return [Vaccination(*row) for row in cursor.fetchall()]

    def delete(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vaccinations WHERE id = ?", (record_id,))
            conn.commit()

    def fetch_by_id(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vaccinations WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            return Vaccination(*row) if row else None

    def fetch_all(self, pet_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vaccinations WHERE pet_id = ? ORDER BY next_due ASC", (pet_id,))
            return [Vaccination(*row) for row in cursor.fetchall()]

    def get_all(self):
        """Fetch all vaccination records."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pet_id, vaccine_name, date_administered, next_due, price, notes FROM vaccinations")
            return [Vaccination(*row) for row in cursor.fetchall()]