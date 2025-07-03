# File: backend/db/vet_visit_db_handler.py
import sqlite3
import os
from backend.models.vet_visit import VetVisit

class VetVisitDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', 'data', 'vet_visits.db')

    def connect(self):
        return sqlite3.connect(self.db_path)

    def insert(self, visit: VetVisit):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO vet_visits (pet_id, visit_date, reason, notes, cost)
                VALUES (?, ?, ?, ?, ?)
                """,
                (visit.pet_id, visit.visit_date, visit.reason, visit.notes, visit.cost)
            )
            conn.commit()
            return cursor.lastrowid

    def update(self, visit: VetVisit):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE vet_visits
                SET pet_id = ?, visit_date = ?, reason = ?, notes = ?, cost = ?
                WHERE id = ?
                """,
                (visit.pet_id, visit.visit_date, visit.reason, visit.notes, visit.cost)
            )
            conn.commit()

    def get_by_pet_id(self, pet_id: int) -> list[VetVisit]:
        """Get all vet visits for a specific pet ID"""
        with self.connect() as conn:
            cursor = conn.cursor()
            # Removed the pet existence check since it's causing errors
            cursor.execute("""
                SELECT pet_id, visit_date, reason, notes, cost
                FROM vet_visits
                WHERE pet_id = ?
                ORDER BY visit_date DESC
            """, (pet_id,))
            return [VetVisit(*row) for row in cursor.fetchall()]

    def delete(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vet_visits WHERE id = ?", (record_id,))
            conn.commit()

    def fetch_by_id(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vet_visits WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            return VetVisit(*row) if row else None

    def fetch_all(self, pet_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vet_visits WHERE pet_id = ? ORDER BY visit_date DESC", (pet_id,))
            return [VetVisit(*row) for row in cursor.fetchall()]

    def get_all(self):
        """Fetch all vet visit records."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pet_id, visit_date, reason, notes, cost FROM vet_visits")
            return [VetVisit(*row) for row in cursor.fetchall()]
        

vet_visits_db_handler = VetVisitDB()