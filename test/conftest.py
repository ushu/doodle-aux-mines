from typing import final
import pytest
from databases import Database
from httpx import AsyncClient
import pytest_asyncio

from db import get_database
from main import app
from config import Config


# Standard setup, against test_database_url this time
config = Config()
test_database = Database(config.test_database_url, force_rollback=True)

# We inject the database in the app
def override_get_db():
    return test_database
app.dependency_overrides[get_database] = override_get_db

# connect to the DB in all the tests (!)
# -> this actually replaces the lifespan parameter of the FastAPI app
@pytest_asyncio.fixture(autouse=True)
async def connect_database():
    await test_database.connect()
    try:
        yield
    finally:
        await test_database.disconnect()