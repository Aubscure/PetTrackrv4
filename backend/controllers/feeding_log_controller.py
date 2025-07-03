# File: backend/controllers/feeding_log_controller.py
from .base_controller import BaseController
from backend.models.feeding_log import FeedingLog
from backend.database_handlers.feeding_logs_db_handler import FeedingLogDB

class FeedingLogController(BaseController):
    def __init__(self):
        super().__init__(FeedingLogDB(), FeedingLog)
        self.db_handler = FeedingLogDB()

    def get_by_pet_id(self, pet_id: int) -> list[FeedingLog]:
        try:
            return self.db_handler.get_by_pet_id(pet_id)
        except Exception as e:
            print(f"Error fetching daycare enrollments: {e}")
            return []