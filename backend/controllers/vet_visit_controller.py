# backend/controllers/vet_visit_controller.py
from .base_controller import BaseController
from backend.models.vet_visit import VetVisit
from backend.database_handlers.vet_visits_db_handler import VetVisitDB 

class VetVisitController(BaseController):
    def __init__(self):
        super().__init__(VetVisitDB(), VetVisit)
        self.db_handler = VetVisitDB()
    
    def get_by_pet_id(self, pet_id: int) -> list[VetVisit]:
        try:
            return self.db_handler.get_by_pet_id(pet_id)
        except Exception as e:
            print(f"Error fetching vet visits: {e}")
            return []