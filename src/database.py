from pymongo import MongoClient
from pymongo.database import Database

from config import MONGO_CONNECTION_URI, MONGO_DATABASE


def get_database() -> Database:
    """Creates a conntection to the database and returns it."""
    client = MongoClient(MONGO_CONNECTION_URI)
    return client[MONGO_DATABASE]
