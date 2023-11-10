"""Module for classes `Player` and `HistoricalEvent`."""

import os

from dataclasses import dataclass, field
from typing import List, Optional

from aiogram.types import FSInputFile

from config import BASE_PATH


@dataclass
class Player:
    """Class representing a player object.

    Properties:
        _id: Player's unique identifier.
        current_event: Id of current event in the game. If None player is not
                       in the game.
        guessed_events: List of events ids which player already guessed.
        attempts: Number of attempts player made to guess current event.
        score: Total score of player.
        in_game: Indicates if player is in the game.

    """

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
    """Class representing a historical event object.

    Properties:
        _id: Unique identifier for historical event.
        _type: Type of event.
        event: Short event description to guess.
        date: Event date in integer format.
        description: Additional information about the event.
        image_path: Path to the event image.

    """

    _id: int
    _type: str
    event: str
    date: int
    description: Optional[str] = None
    image_path: Optional[str] = None

    def get_image_file(self) -> Optional[FSInputFile]:
        """Returns the event image file or `None` if file does not exist."""
        if self.image_path:
            path = os.path.join(BASE_PATH, self.image_path)
            return FSInputFile(path) if os.path.isfile(path) else None

    def explain(self) -> str:
        """Returns explanation for event with date and short description."""
        return "{} г. - {}.".format(self.date, self.event)
