# backend/controllers/base_controller.py
class BaseController:
    def __init__(self, db_handler, model_class):
        self.db = db_handler
        self.Model = model_class

    def create(self, data: dict):
        instance = self.Model(**data)
        return self.db.insert(instance)

    def update(self, record_id: int, data: dict):
        data['id'] = record_id
        instance = self.Model(**data)
        return self.db.update(instance)

    def delete(self, record_id: int):
        return self.db.delete(record_id)

    def get_by_id(self, record_id: int):
        return self.db.fetch_by_id(record_id)

    def get_all_by_pet(self, pet_id: int):
        return self.db.fetch_all(pet_id=pet_id)