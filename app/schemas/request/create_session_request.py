from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    user_id: int
    variant_id: str   # VD: "v_us"
    scenario_id: str  # VD: "sc_restaurant"
    context_id: str   # VD: "ctx_order_steak"