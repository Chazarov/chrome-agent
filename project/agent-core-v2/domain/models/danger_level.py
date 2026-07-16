from pydantic import BaseModel

class DangerLevelBase(BaseModel):
    id: int
    name: str
    description: str

class DangerLevel(DangerLevelBase):
    prev_state: DangerLevelBase