"""Module to manage the project configuration settings."""
import os
from pathlib import Path

from dotenv import load_dotenv


# Parse a `.env` file and load the variables inside into environment variables
load_dotenv()


class ImproperlyConfigured(Exception):
    """Raises when a environment variable is missing."""

    def __init__(self, variable_name, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


def get_env_variable(var_name: str) -> str:
    """Get an environment variable or raise an exception.

    Args:
        var_name: a name of a environment variable.

    Returns:
        A value of the environment variable.

    Raises:
        ImproperlyConfigured: if the environment variable is not set.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(var_name)


BASE_PATH: str = Path(__file__).resolve().parent.parent
RESOURCES_PATH: str = os.path.join(BASE_PATH, "res/")

BOT_TOKEN: str = get_env_variable("BOT_TOKEN")

MONGO_CONNECTION_STRING: str = get_env_variable("MONGO_CONNECTION")
MONGO_DATABASE_NAME: str = get_env_variable("MONGO_DATABASE_NAME")
