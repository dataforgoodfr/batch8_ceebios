import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv("../../.env")


class Settings(BaseSettings):
    PROJECT_NAME: str = "POKEDEX API"
    PROJECT_DESCRIPTION: str = "Open source API to access research papers related to biodiversity and biomimetism!"
    API_BASE: str = "api/"
    VERSION: str = "0.1.0"
    DATABASE_URI = str = os.getenv("DATABASE_URI")
    DATABASE_NAME = str = os.getenv("DATABASE_NAME")


settings = Settings()
