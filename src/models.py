import os

from dataclasses import dataclass, field
from typing import List, Optional

from aiogram.types import FSInputFile

from config import BASE_PATH


@dataclass
class Player:
    _id: int
    current_event: Optional[int] = None
    guessed_events: List[int] = field(default_factory=list)
    attempts: int = 0
    score: int = 0

    @property
    def in_game(self) -> bool:
        return isinstance(self.current_event, int)


@dataclass
class HistoricalEvent:
    _id: int
    _type: str
    event: str
    date: int
    description: Optional[str] = None
    image_path: Optional[str] = None

    def get_image_file(self) -> Optional[FSInputFile]:
        if self.image_path:
            path = os.path.join(BASE_PATH, self.image_path)
            return FSInputFile(path) if os.path.isfile(path) else None

    def explain(self) -> str:
        return "{} г. - {}.".format(self.date, self.event)
