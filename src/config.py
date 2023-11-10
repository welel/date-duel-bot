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


def get_env_variable(var_name: str, cast=str) -> str:
    """Get an environment variable or raise an exception.

    Args:
        var_name: a name of a environment variable.

    Returns:
        A value of the environment variable.

    Raises:
        ImproperlyConfigured: if the environment variable is not set.
    """
    try:
        return cast(os.environ[var_name])
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except TypeError:
        raise TypeError(f"Variable {var_name} must be type {cast}.")


BASE_PATH: str = Path(__file__).resolve().parent.parent
RESOURCES_PATH: str = os.path.join(BASE_PATH, "res/")

BOT_TOKEN: str = get_env_variable("BOT_TOKEN")

MONGO_HOST: str = get_env_variable("MONGO_HOST")
MONGO_PORT: int = get_env_variable("MONGO_PORT", cast=int)
MONGO_USERNAME: str = get_env_variable("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD: str = get_env_variable("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DATABASE: str = get_env_variable("MONGO_INITDB_DATABASE")
MONGO_CONNECTION_URI: str = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
)
