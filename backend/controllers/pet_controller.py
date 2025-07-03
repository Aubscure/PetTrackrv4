import os
import sqlite3
import shutil
import re
from typing import List, Tuple, Optional
from datetime import datetime
from backend.models.pet import Pet, Owner


class PetController:
    """Handles all database operations for Pets and Owners following SOLID principles."""
    
    def __init__(self, db_path: str = None):
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.images_dir = os.path.join(self.data_dir, 'images')
        self.db_path = db_path or os.path.join(self.data_dir, 'pets.db')
        
        self._initialize_directories()
        self._enable_foreign_keys()

    def _initialize_directories(self) -> None:
        """Ensures required directories exist."""
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

    def _enable_foreign_keys(self) -> None:
        """Activates SQLite foreign key constraints."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a database connection with foreign keys enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def add_pet_with_owner(self, pet: Pet, owner: Owner, image_path: Optional[str] = None) -> int:
        """
        Adds a pet with owner details and optional image.
        
        Args:
            pet: Pet instance with required attributes
            owner: Owner instance with contact info
            image_path: Optional path to pet image
            
        Returns:
            ID of the newly created pet
            
        Raises:
            sqlite3.Error: If database operation fails
            IOError: If image file cannot be processed
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Transaction starts
                owner_id = self._upsert_owner(cursor, owner)
                pet_id = self._insert_pet(cursor, pet, owner_id)
                
                if image_path:
                    stored_image_path = self._process_image(pet, pet_id, image_path)
                    self._update_pet_image(cursor, pet_id, stored_image_path)
                
                conn.commit()
                return pet_id
                
        except (sqlite3.Error, IOError) as e:
            conn.rollback()
            raise RuntimeError(f"Failed to add pet: {str(e)}") from e

    def _upsert_owner(self, cursor: sqlite3.Cursor, owner: Owner) -> int:
        """Inserts or updates owner, returns owner ID."""
        cursor.execute('''
            INSERT INTO owner (name, contact_number, address)
            VALUES (?, ?, ?)
            ON CONFLICT(name, contact_number) DO UPDATE SET
                address = excluded.address
            RETURNING id
        ''', (owner.name, owner.contact_number, owner.address))
        
        result = cursor.fetchone()
        return result[0] if result else None

    def _insert_pet(self, cursor: sqlite3.Cursor, pet: Pet, owner_id: int) -> int:
        """Inserts pet record and returns new pet ID."""
        cursor.execute('''
            INSERT INTO pets (name, breed, birthdate, owner_id)
            VALUES (?, ?, ?, ?)
            RETURNING id
        ''', (pet.name, pet.breed, pet.birthdate, owner_id))
        
        return cursor.fetchone()[0]

    def _process_image(self, pet: Pet, pet_id: int, src_path: str) -> str:
        """Stores pet image and returns relative path."""
        ext = os.path.splitext(src_path)[1].lower()
        safe_name = re.sub(r'[^a-z0-9]', '_', pet.name.lower())
        filename = f"{safe_name}_{pet_id}{ext}"
        dest_path = os.path.join(self.images_dir, filename)
        
        shutil.copy2(src_path, dest_path)
        return os.path.relpath(dest_path, start=self.data_dir)

    def _update_pet_image(self, cursor: sqlite3.Cursor, pet_id: int, image_path: str) -> None:
        """Updates pet record with image path."""
        cursor.execute('''
            UPDATE pets SET image_path = ? WHERE id = ?
        ''', (image_path, pet_id))

    def get_pet_by_id(self, pet_id: int) -> Tuple[Optional[Pet], Optional[Owner]]:
        """
        Retrieves a single pet by ID with its owner information.
        
        Args:
            pet_id: ID of the pet to retrieve
            
        Returns:
            Tuple of (Pet, Owner) if found, (None, None) otherwise
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.id AS pet_id, p.name AS pet_name, p.breed, p.birthdate, p.image_path,
                    o.id AS owner_id, o.name AS owner_name, o.contact_number, o.address
                FROM pets p
                LEFT JOIN owner o ON p.owner_id = o.id
                WHERE p.id = ?
            ''', (pet_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None, None
                
            pet = Pet(
                id=row['pet_id'],
                name=row['pet_name'],
                breed=row['breed'],
                birthdate=row['birthdate'],
                image_path=row['image_path'],
                owner_id=row['owner_id']
            )
            
            owner = Owner(
                id=row['owner_id'],
                name=row['owner_name'],
                contact_number=row['contact_number'],
                address=row['address']
            ) if row['owner_id'] else None
            
            return pet, owner

    def get_pets_with_owners(self) -> Tuple[List[Pet], List[Optional[Owner]]]:
        """
        Retrieves all pets with their associated owner information.
        
        Returns:
            Tuple of (list of Pets, list of corresponding Owners)
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.id AS pet_id, p.name AS pet_name, p.breed, p.birthdate, p.image_path,
                    o.id AS owner_id, o.name AS owner_name, o.contact_number, o.address
                FROM pets p
                LEFT JOIN owner o ON p.owner_id = o.id
            ''')
            
            pets = []
            owners = []
            
            for row in cursor.fetchall():
                pet = Pet(
                    id=row['pet_id'],
                    name=row['pet_name'],  # Changed to pet_name
                    breed=row['breed'],
                    birthdate=row['birthdate'],
                    image_path=row['image_path'],
                    owner_id=row['owner_id']
                )
                
                owner = Owner(
                    id=row['owner_id'],
                    name=row['owner_name'],  # Changed to owner_name
                    contact_number=row['contact_number'],
                    address=row['address']
                ) if row['owner_id'] else None
                
                pets.append(pet)
                owners.append(owner)
            
            return pets, owners

    def get_owner_by_id(self, owner_id: int) -> Optional[Owner]:
        """Retrieves a single owner by ID."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, contact_number, address 
                FROM owner 
                WHERE id = ?
            ''', (owner_id,))
            
            row = cursor.fetchone()
            return Owner(**dict(row)) if row else None

    def get_all_owners(self) -> List[Owner]:
        """Retrieves all owners from the database."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, contact_number, address 
                FROM owner
            ''')
            
            return [Owner(**dict(row)) for row in cursor.fetchall()]

    def get_pets_with_vacc_and_vet_records(self):
        """
        Returns pets that have at least one vaccination AND at least one vet visit record.
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT p.*
                FROM pets p
                INNER JOIN vaccinations vax ON p.id = vax.pet_id
                INNER JOIN vet_visits vv ON p.id = vv.pet_id
            """)
            pets = [self._row_to_pet(row) for row in cursor.fetchall()]
            return pets

    def _row_to_pet(self, row: sqlite3.Row) -> Pet:
        """Converts a database row to a Pet object."""
        return Pet(
            id=row['id'],
            name=row['name'],
            breed=row['breed'],
            birthdate=row['birthdate'],
            owner_id=row['owner_id'],
            image_path=row.get('image_path')  # image_path may not always be present
        )

    def get_pets_with_vacc_or_vet_records(self):
        """
        Returns pets (with owners) that have at least one vaccination OR at least one vet visit record.
        Works even if vaccinations and vet_visits are in separate DB files.
        """
        from backend.controllers.vaccination_controller import VaccinationController
        from backend.controllers.vet_visit_controller import VetVisitController

        pets, owners = self.get_pets_with_owners()
        pets_with_records = []
        owners_with_records = []

        vax_ctrl = VaccinationController()
        visit_ctrl = VetVisitController()

        for pet, owner in zip(pets, owners):
            has_vax = vax_ctrl.get_by_pet_id(pet.id)
            has_visit = visit_ctrl.get_by_pet_id(pet.id)
            if has_vax or has_visit:
                pets_with_records.append(pet)
                owners_with_records.append(owner)

        return pets_with_records, owners_with_records

    def get_pets_with_feeding_logs(self):
        """
        Returns pets (with owners) that have at least one feeding log.
        """
        from backend.controllers.feeding_log_controller import FeedingLogController

        pets, owners = self.get_pets_with_owners()
        pets_with_logs = []
        owners_with_logs = []

        feeding_ctrl = FeedingLogController()

        for pet, owner in zip(pets, owners):
            logs = feeding_ctrl.get_by_pet_id(pet.id)
            if logs:
                pets_with_logs.append(pet)
                owners_with_logs.append(owner)

        return pets_with_logs, owners_with_logs