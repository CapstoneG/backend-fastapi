from app.repositories.variant_repository import VariantRepository
from app.schemas.variant_response import VariantResponse
from app.schemas.request.variant_request import VariantRequest

class VariantService:
    def __init__(self):
        self.repository = VariantRepository()

    def get_all_variants(self):
        variants = self.repository.find_all()
        return [self.to_response(variant) for variant in variants]
    
    def save(self, request: VariantRequest):
        variant = self.repository.save(request=request)
        return self.to_response(variant=variant)

    def to_response(self, variant):
        return VariantResponse(
            id = str(variant.get('_id')),
            name = variant.get('name'),
            flag_icon = variant.get('flag_icon'),
            system_instruction_add_on= variant.get('system_instruction_add_on')
        )