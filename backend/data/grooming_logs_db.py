# File: backend/data/grooming_logs_db.py
import sqlite3
import os

class GroomingLogsDatabaseInitializer:
    """
    Handles initialization of the grooming_logs.db database and creation of the grooming_logs table.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '..', 'data')
        self.db_path = os.path.join(self.data_dir, 'grooming_logs.db')

    def initialize(self):
        """Creates the grooming_logs table if it does not already exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grooming_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    groom_date TEXT DEFAULT (datetime('now')),
                    groom_type TEXT,
                    price REAL,
                    groomer_name TEXT,
                    notes TEXT,
                    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

# Optional standalone run
if __name__ == "__main__":
    GroomingLogsDatabaseInitializer().initialize()