"""Logic for date guessing game."""
from typing import Dict, Optional, Tuple

from models import HistoricalEvent, Player
from dao import PlayerDao, HistoricalEventDao


class GuessGame:
    events: Dict[int, HistoricalEvent]
    players_dao: PlayerDao
    players: Dict[int, Player]

    def __init__(self, database):
        events_dao = HistoricalEventDao(database)
        self.events = {event._id: event for event in events_dao.all()}
        self.players_dao = PlayerDao(database)
        self.players = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.players_dao.save_many(self.players.values())

    def get_player(self, player_id: int) -> Player:
        player = self.players.get(player_id)
        if not player:
            player = self.players_dao.get(player_id)
            self.players[player_id] = player
        return player

    def _get_event_for_player(self, player: Player) -> HistoricalEvent:
        for event in self.events.values():
            if event._id not in player.guessed_events:
                return event
        player.guessed_events = []
        return self._get_event_for_player(player)

    def play(self, player_id: int) -> HistoricalEvent:
        player = self.get_player(player_id)
        event = self._get_event_for_player(player)
        player.current_event = event._id
        self.players[player._id] = player
        return event

    def guess(
        self, player: Player, date: int
    ) -> Tuple[str, Optional[HistoricalEvent]]:
        event = self.events[player.current_event]
        player.attempts += 1
        if event.date == date:
            player.guessed_events.append(player.current_event)
            player.current_event = None
            player.score += 10
            self.players[player._id] = player
            return "Ты угадал, ура!", event
        else:
            player.score -= 1
            self.players[player._id] = player
            if date > event.date:
                return "Это произошло раньше.", None
            else:
                return "Это произошло позже.", None

    def surrender(self, player: Player) -> HistoricalEvent:
        event = self.events[player.current_event]
        player.current_event = None
        player.score -= 10
        self.players[player._id] = player
        return event

    def cancel(self, player: Player):
        player.current_event = None
        self.players[player._id] = player
