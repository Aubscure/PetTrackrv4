# File: backend/data/pets_db.py
import sqlite3
import os

class PetDatabaseInitializer:
    """
    Handles initialization of the pets.db database and creation of the tables.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '..', 'data')
        self.db_path = os.path.join(self.data_dir, 'pets.db')

    def initialize(self):
        """Creates the database tables if they don't exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create owner table first (since pets references it)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS owner (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_number INTEGER,
                    address TEXT,
                    UNIQUE(name, contact_number)
                );
            ''')
            
            # Then create pets table (FOREIGN KEY references owner(id), not owners(id))
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    breed TEXT,
                    birthdate TEXT,
                    image_path TEXT,
                    owner_id INTEGER NOT NULL,
                    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE
                );
            ''')

            conn.commit()

# Optional standalone run
if __name__ == "__main__":
    PetDatabaseInitializer().initialize()