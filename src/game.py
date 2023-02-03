"""Logic for the date guessing game.

This module contains the implementation of a guess game where players
try to guess the year of historical events. The game uses the `Player`
and `HistoricalEvent` model classes and the `PlayerDao` and
`HistoricalEventDao` data access objects for storing and retrieving player
and historical event data from the database.

"""
from typing import Dict, Optional, Tuple

from models import HistoricalEvent, Player
from dao import PlayerDao, HistoricalEventDao


class GuessGame:
    """Implementation of a guess date game.

    Properties:
        events: A dictionary mapping from historical event id
                to `HistoricalEvent` instance.
        players_dao: An instance of `PlayerDao` for accessing the player data
                     in the database.
        players: A dictionary mapping from player id to `Player` instance;
                 stores cached players.

    """

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
        """Saves all cached players to the database on exit."""
        self.players_dao.save_many(self.players.values())

    def get_player(self, player_id: int) -> Player:
        """Gets a player by id from the cache if exists otherviese from DB.

        Retrives a player for the cache if it exists otherviese from
        the database and saves the player to the cache.

        Args:
            player_id: Player's unique identifier to retrive.

        Returns:
            The player instance with given id.
        """
        player = self.players.get(player_id)
        if not player:
            player = self.players_dao.get(player_id)
            self.players[player_id] = player
        return player

    def _get_event_for_player(self, player: Player) -> HistoricalEvent:
        """Returns a not gussed event for a specifiec player.

        If all events gussed resets player's guessed events and starts over.

        Args:
            player: A player instance for picking next event.

        Returns:
            A next historival event for guessing.
        """
        for event in self.events.values():
            if event._id not in player.guessed_events:
                return event
        player.guessed_events = []
        return self._get_event_for_player(player)

    def play(self, player_id: int) -> HistoricalEvent:
        """Starts a new game round for a given player.

        Retrieves the `Player` instance, sets the `current_event` for
        the player, and returns the `current_event`.

        Args:
            player_id: Player's unique identifier to start a new game round with.

        Returns:
            A next historival event for guessing.
        """
        player = self.get_player(player_id)
        event = self._get_event_for_player(player)
        player.current_event = event._id
        self.players[player._id] = player
        return event

    def guess(
        self, player: Player, date: int
    ) -> Tuple[str, Optional[HistoricalEvent]]:
        """Processes a player's guess.

        Given a `Player` instance and a player's guess (`date`).
        Updates the player's attempts, and returns a message indicating
        whether the guess was correct and the corresponding `HistoricalEvent`
        instance if the guess was correct.

        Args:
            player: A player instance that trying to guess.
            date: A player's guess.

        Returns:
            Tuple - message (a hint for guessing or success message),
                    the event if guessed, `None` othervise.
        """
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
        """Ends a game round and returns the hidden event.

        Given a `Player` instance, updates the player's score, sets the
        `current_event` for the player to `None`, and returns the `current_event`.

        Args:
            player: A surrendered player.

        Returns:
            The hidden event.
        """
        event = self.events[player.current_event]
        player.current_event = None
        player.score -= 10
        self.players[player._id] = player
        return event

    def cancel(self, player: Player):
        player.current_event = None
        self.players[player._id] = player
