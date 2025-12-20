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
    
    def get_scenario_context_details(self, scenario_id: str, context_id: str):
        """
        Lấy tên Scenario và mô tả chi tiết của Context
        Vì Context nhúng trong Scenario nên phải query Scenario trước
        """
        doc = self.collection.find_one({"_id": scenario_id})
        if not doc:
            return "Unknown Scenario", "General Conversation"
        
        scenario_name = doc.get("name", "Unknown")
        
        # Tìm context cụ thể trong mảng contexts
        context_desc = "General conversation"
        initial_msg = ""
        
        for ctx in doc.get("contexts", []):
            if ctx["id"] == context_id:
                context_desc = ctx.get("description", "")
                initial_msg = ctx.get("initial_ai_message", "")
                break
                
        return scenario_name, context_desc