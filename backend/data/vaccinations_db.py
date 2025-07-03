# File: backend/data/vaccinations_db.py
import sqlite3
import os

class VaccinationsDatabaseInitializer:
    """
    Handles initialization of the vaccinations.db database and creation of the vaccinations table.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '..', 'data')
        self.db_path = os.path.join(self.data_dir, 'vaccinations.db')

    def initialize(self):
        """Creates the vaccinations table if it does not already exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vaccinations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    vaccine_name TEXT,
                    date_administered TEXT,
                    next_due TEXT,
                    price INTEGER,      -- NEW: predetermined price per vaccine
                    notes TEXT,         -- Optional notes (e.g. side effects, vet remarks)
                    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
                )
            ''')

            conn.commit()

# Optional standalone run
if __name__ == "__main__":
    VaccinationsDatabaseInitializer().initialize()