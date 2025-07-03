# File: backend/data/feeding_logs_db.py
import sqlite3
import os

class FeedingLogsDatabaseInitializer:
    """
    Handles initialization of the feeding_logs.db database and creation of the feeding_logs table.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '..', 'data')
        self.db_path = os.path.join(self.data_dir, 'feeding_logs.db')

    def initialize(self):
        """Creates the feeding_logs table if it does not already exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daycare_enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    num_days INTEGER NOT NULL,
                    feed_once BOOLEAN DEFAULT 0,
                    feed_twice BOOLEAN DEFAULT 0,
                    feed_thrice BOOLEAN DEFAULT 0,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
                )
            ''')

            conn.commit()

# Optional standalone run
if __name__ == "__main__":
    FeedingLogsDatabaseInitializer().initialize()