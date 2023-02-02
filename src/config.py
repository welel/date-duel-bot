import os
from pathlib import Path

from dotenv import load_dotenv


# Parse a `.env` file and load the variables inside into environment variables
load_dotenv()

BASE_PATH = Path(__file__).resolve().parent.parent
RESOURCES_PATH = os.path.join(BASE_PATH, "res/")

BOT_TOKEN: str = os.getenv("BOT_TOKEN")

MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION")
MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME")
