from pymongo import MongoClient
from pymongo.database import Database

from config import MONGO_CONNECTION_STRING, MONGO_DATABASE_NAME


def get_database() -> Database:
    client = MongoClient(MONGO_CONNECTION_STRING)
    return client[MONGO_DATABASE_NAME]
