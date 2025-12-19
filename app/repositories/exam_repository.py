from app.db.mongodb import db
from bson import ObjectId
from bson.errors import InvalidId

class ExamRepository:
    def __init__(self):
        self.collection = db['toeic_exams']

    def find_all(self):
        return list(self.collection.find())
    
    def find_by_title(self, title: str):
        return self.collection.find_one({'exam_title': title})
    
    def find_by_id(self, exam_id: str):
        try:
            obj_id = ObjectId(exam_id)
        except InvalidId:
            return None
        return self.collection.find_one({'_id': obj_id})
    
    def find_by_part(self, part_name: str):
        return list(self.collection.find({f'parts.{part_name}': {'$exists': True}}))
    
    def save(self, exam_data: dict):
        result = self.collection.insert_one(exam_data)
        return str(result.inserted_id)