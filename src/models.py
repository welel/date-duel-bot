from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Player:
    _id: int
    current_event: Optional[int] = None
    guessed_events: List[int] = field(default_factory=list)
    attempts: int = 0
    score: int = 0


@dataclass
class HistoricalEvent:
    _id: int
    _type: str
    event: str
    date: int
    description: Optional[str] = None
    image_path: Optional[str] = None
