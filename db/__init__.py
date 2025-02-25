from contextlib import asynccontextmanager
from typing import Annotated

from databases import Database
from fastapi import Depends
from config import Config

config = Config()

# And set a database
database = Database(config.database_url)

def get_database():
    return database

DB = Annotated[dict, Depends(get_database)]
