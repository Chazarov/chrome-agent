from abc import abstractmethod
from typing import Protocol
from domain.models import DangerLevel, DangerReason


class Notificator(Protocol):
    @abstractmethod
    def danger_level_notify(self, danger_level: DangerLevel, reason: DangerReason): ...


    @abstractmethod
    def warning_notify(self, warning: str): ...
