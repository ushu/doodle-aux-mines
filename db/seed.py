from pathlib import Path
local_dir = Path(__file__).parent.absolute()
root_dir = Path(__file__).parent.parent.absolute()

# We hack the path to be able to import the config
import sys
sys.path.append(f"{root_dir}/")
from config import Config

# And at last, we can do the work 😅
import asyncio
from databases import Database

config = Config()

async def seed(database_url: str):
    database = Database(database_url)
    await database.connect()
    await run_script(database, local_dir.joinpath('structure.sql'))
    await database.disconnect()

async def run_script(database: Database, script_path: str):
    # Lecture du fichier seed.sql
    sql_script = Path(script_path).read_text()
    
    # Exécution du script SQL
    for statement in sql_script.split(';'):
        if statement.strip():
            await database.execute(statement)

if __name__ == "__main__":
    asyncio.run(seed(config.database_url))
    asyncio.run(seed(config.test_database_url))