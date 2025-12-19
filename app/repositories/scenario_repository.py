from app.db.mongodb import db
from app.schemas.request.scenario_request import ScenarioModel

class ScenarioRepository:
    def __init__(self):
        self.collection = db['scenarios']

    def find_all(self):
        return self.collection.find()
    
    def save(self, request: ScenarioModel):
        scenario = request.model_dump(by_alias=True)
        self.collection.insert_one(scenario)
        return scenario
    
    def find_all_by_variant(self, variant_id: str):
        query = {
            "$or": [
                {"available_variants": []}, 
                {"available_variants": "v_us"}
            ]
        }
        return self.collection.find(query).to_list()