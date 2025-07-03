# backend/controllers/vaccination_controller.py
from .base_controller import BaseController
from backend.models.vaccination import Vaccination
from backend.database_handlers.vaccinations_db_handler import VaccinationDB

class VaccinationController(BaseController):
    def __init__(self):
        super().__init__(VaccinationDB(), Vaccination)
        self.db_handler = VaccinationDB()

    def get_by_pet_id(self, pet_id: int) -> list[Vaccination]:
        try:
            return self.db_handler.get_by_pet_id(pet_id)
        except Exception as e:
            print(f"Error fetching vaccinations: {e}")
            return []