from pydantic import BaseModel


class DangerReason(BaseModel):
    name: str
    description: str
    id: int