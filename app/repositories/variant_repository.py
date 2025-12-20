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
    
    def get_variant_instruction(self, variant_id: str) -> str:
        """Lấy hướng dẫn system instruction của giọng (VD: Anh Mỹ)"""
        # Giả sử variant_id lưu trong DB là string "v_us" hoặc ObjectId
        doc = self.collection.find_one({"_id": variant_id})
        if doc:
            return doc.get("system_instruction", "Speak standard English.")
        return "Speak standard English."