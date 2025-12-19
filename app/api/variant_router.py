from fastapi import APIRouter
from app.services.variant_service import VariantService
from app.schemas.variant_response import VariantResponse
from app.schemas.request.variant_request import VariantRequest
from app.schemas.request.scenario_request import ScenarioModel
from app.schemas.scenario_response import ScenarioResponse
from app.services.scenario_service import ScenarioService
from typing import List, Optional

router = APIRouter(prefix='/variants', tags=["Variant"])
variant_service = VariantService()
scenario_service = ScenarioService()

@router.get('', response_model=List[VariantResponse])
def get_all_variants():
    return variant_service.get_all_variants()

@router.post('', response_model=VariantResponse)
def create_variant(request: VariantRequest):
    return variant_service.save(request=request)

@router.get('/scenarios', response_model=List[ScenarioResponse])
def get_all_scenarios():
    return scenario_service.get_all_scenarios()

@router.post('/scenarios', response_model=ScenarioResponse)
def create_scenario(request: ScenarioModel):
    return scenario_service.save(request)

@router.post('/scenarios', response_model=ScenarioResponse)
def create_scenario(request: ScenarioModel):
    return scenario_service.save(request)

@router.get('/scenarios', response_model=List[ScenarioResponse])
def get_scenarios(variant_id: Optional[str] = None):
    if variant_id:
        return scenario_service.find_scenarios_by_variant(variant_id)
    return scenario_service.get_all_scenarios()