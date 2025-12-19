from pydantic import BaseModel, Field

class VariantRequest(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    flag_icon: str
    system_instruction_add_on: str

    model_config = {
        "populate_by_name": True
    }