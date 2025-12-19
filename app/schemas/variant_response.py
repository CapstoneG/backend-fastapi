from pydantic import BaseModel, Field

class VariantResponse(BaseModel):
    id: str 
    name: str
    flag_icon: str
    system_instruction_add_on: str