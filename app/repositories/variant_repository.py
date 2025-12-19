from app.db.mongodb import db
from app.schemas.request.variant_request import VariantRequest

class VariantRepository:
    def __init__(self):
        self.collection = db["variants"]

    def find_all(self):
        return list(self.collection.find())
    
    def save(self, request: VariantRequest):
        variant = request.model_dump(by_alias=True)
        self.collection.insert_one(variant)
        return variant