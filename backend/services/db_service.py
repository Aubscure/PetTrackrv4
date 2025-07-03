# backend/services/db_service.py

import sqlite3
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def test_db_connection(db_filename):
    db_path = f'/{db_filename}'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"🟢 Connected to {db_filename}")
        print("    Tables:", tables)
        conn.close()
    except Exception as e:
        print(f"🔴 Failed to connect to {db_filename}:", e)

def test_all_connections():
    db_files = [
        'pets.db',
        'vet_visits.db',
        'vaccinations.db',
        'feeding_logs.db',
        'grooming_logs.db',
        'health_notes.db'
    ]
    print("📁 Testing all database connections:\n")
    for db_file in db_files:
        test_db_connection(db_file)
    print("\n✅ Database connectivity check complete.")

if __name__ == "__main__":
    test_all_connections()