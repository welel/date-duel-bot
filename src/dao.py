from typing import List, Tuple

from pymongo import ReplaceOne
from pymongo.database import Database

from models import HistoricalEvent, Player


class ObjectDoesNotExists(Exception):
    """Raises when a document is not exists in the database."""

    pass


class HistoricalEventDao:
    data_source: Database
    collection_name: str = "HistoricalEvents"

    def __init__(self, data_source: Database):
        self.data_source = data_source[self.collection_name]

    def all(self) -> List:
        return [HistoricalEvent(**event) for event in self.data_source.find()]


class PlayerDao:
    data_source: Database
    collection_name: str = "Players"

    def __init__(self, data_source: Database):
        self.data_source = data_source[self.collection_name]

    def create(self, player: Player) -> Tuple[Player, bool]:
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
        player = self.data_source.find_one({"_id": player_id})
        if not player:
            raise ObjectDoesNotExists(
                f"Player with id {player_id} does not exists."
            )
        return Player(**player)

    def save_many(self, players: List[Player]):
        if players:
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
