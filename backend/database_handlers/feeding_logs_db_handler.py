# File: backend/database/feeding_logs_db_handler.py
import sqlite3
import os
from backend.models.feeding_log import FeedingLog

class FeedingLogDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', 'data', 'feeding_logs.db')

    def connect(self):
        return sqlite3.connect(self.db_path)

    def insert(self, log: FeedingLog):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO daycare_enrollments 
                (pet_id, start_date, num_days, feed_once, feed_twice, feed_thrice, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                log.pet_id,
                log.start_date,
                log.num_days,
                int(log.feed_once),
                int(log.feed_twice),
                int(log.feed_thrice),
                log.notes
            ))
            conn.commit()
            return cursor.lastrowid

    def update(self, record_id: int, log: FeedingLog):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE daycare_enrollments
                SET pet_id = ?, start_date = ?, num_days = ?, 
                    feed_once = ?, feed_twice = ?, feed_thrice = ?, notes = ?
                WHERE id = ?
            """, (
                log.pet_id,
                log.start_date,
                log.num_days,
                int(log.feed_once),
                int(log.feed_twice),
                int(log.feed_thrice),
                log.notes,
                record_id
            ))
            conn.commit()

    def get_by_pet_id(self, pet_id: int) -> list[FeedingLog]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pet_id, start_date, num_days, feed_once, feed_twice, feed_thrice, notes
                FROM daycare_enrollments
                WHERE pet_id = ?
            """, (pet_id,))
            return [FeedingLog(*row) for row in cursor.fetchall()]

    def delete(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM daycare_enrollments WHERE id = ?", (record_id,))
            conn.commit()

    def fetch_by_id(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pet_id, start_date, num_days, feed_once, feed_twice, feed_thrice, notes
                FROM daycare_enrollments
                WHERE id = ?
            """, (record_id,))
            row = cursor.fetchone()
            return FeedingLog(*row) if row else None