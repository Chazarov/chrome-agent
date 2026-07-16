from domain.models import DangerLevelBase

class SetDangerLevel(BaseModel):
    danger_level: DangerLevelBase
    