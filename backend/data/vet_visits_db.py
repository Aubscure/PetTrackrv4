# File: backend/data/vet_visits_db.py
import sqlite3
import os

class VetVisitsDatabaseInitializer:
    """
    Handles initialization of the vet_visits.db database and creation of the vet_visits table.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '..', 'data')
        self.db_path = os.path.join(self.data_dir, 'vet_visits.db')

    def initialize(self):
        """Creates the vet_visits table if it does not already exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS vet_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    visit_date TEXT,
                    reason TEXT,
                    notes TEXT,
                    cost REAL,
                    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
                )
            ''')

            conn.commit()

# Optional standalone run
if __name__ == "__main__":
    VetVisitsDatabaseInitializer().initialize()