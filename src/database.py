from pymongo import MongoClient

from config import MONGO_CONNECTION_STRING, MONGO_DATABASE_NAME


def get_database():
    client = MongoClient(MONGO_CONNECTION_STRING)
    return client[MONGO_DATABASE_NAME]
