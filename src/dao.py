"""Module with data access objects (DAO) for MongoDB connection.

Contains two data access objects (DAO): `HistoricalEventDao` and `PlayerDao`.
"""
from typing import List, Tuple

from pymongo import ReplaceOne
from pymongo.database import Database

from models import HistoricalEvent, Player


class ObjectDoesNotExists(Exception):
    """Raises when a document is not exists in the database."""

    pass


class HistoricalEventDao:
    """Class for data access of `HistoricalEvent` records from the Database.

    Properties:
        data_source: The Database object.
        collection_name: The name of the collection in the MongoDB to access
                         `HistoricalEvent` records.

    """

    data_source: Database
    collection_name: str = "HistoricalEvents"

    def __init__(self, data_source: Database):
        self.data_source = data_source[self.collection_name]

    def all(self) -> List[HistoricalEvent]:
        """Retrieve all historical events from the database.

        Returns:
            A list of `HistoricalEvent` objects.
        """
        return [HistoricalEvent(**event) for event in self.data_source.find()]


class PlayerDao:
    """Class for data access of `Player` records from the Database.

    Properties:
        data_source: The Database object.
        collection_name: The name of the collection in the MongoDB to access
                         `Player` records.

    """

    data_source: Database
    collection_name: str = "Players"

    def __init__(self, data_source: Database):
        self.data_source = data_source[self.collection_name]

    def create(self, player: Player) -> Tuple[Player, bool]:
        """Create player and return the player and whether it was created.

        Args:
            player: the player to create.

        Returns:
            The player and a bool flag - whether it was created.
        """
        player_db = self.data_source.find_one({"_id": player._id})
        created = player_db == None

        if player_db:
            player = Player(**player_db)
        else:
            self.data_source.insert_one(
                {
                    "_id": player._id,
                    "current_event": player.current_event,
                    "guessed_events": player.guessed_events,
                    "attempts": player.attempts,
                    "score": player.score,
                }
            )
        return player, created

    def get(self, player_id: int) -> Player:
        """Gets the Player object from the data source with the given player id.

        Args:
            player_id: The id of the player to get.

        Returns:
            The Player object with the given id.

        Raises:
            ObjectDoesNotExists: If the player with the given id doesn't exist
            in the database.
        """
        player = self.data_source.find_one({"_id": player_id})
        if not player:
            raise ObjectDoesNotExists(
                f"Player with id {player_id} does not exists."
            )
        return Player(**player)

    def save_many(self, players: List[Player]):
        """Saves list of players to the database."""
        if not players:
            return

        update_objects = [
            ReplaceOne(
                {"_id": player._id},
                {
                    "current_event": player.current_event,
                    "guessed_events": player.guessed_events,
                    "attempts": player.attempts,
                    "score": player.score,
                },
                upsert=True,
            )
            for player in players
        ]
        self.data_source.bulk_write(update_objects)
