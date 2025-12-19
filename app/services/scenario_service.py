from app.repositories.scenario_repository import ScenarioRepository
from app.schemas.scenario_response import ScenarioResponse
from app.schemas.request.scenario_request import ScenarioModel

class ScenarioService:
    def __init__(self):
        self.repository = ScenarioRepository()

    def get_all_scenarios(self):
        scenarios = self.repository.find_all()
        return [self.to_response(scenario) for scenario in scenarios]
    
    def save(self, scenario: ScenarioModel):
        return self.to_response(self.repository.save(scenario))
    
    def find_scenarios_by_variant(self, variant_id: str):
        return self.to_response(self.repository.find_all_by_variant(variant_id=variant_id))

    def to_response(self, scenario):
        return ScenarioResponse(
            id=str(scenario.get('_id')),
            name=scenario.get('name'),
            description=scenario.get('description'),
            contexts=scenario.get('contexts')
        )