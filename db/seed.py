import asyncio
import os
from databases import Database
from pathlib import Path

dirname = os.path.dirname(__file__)

async def seed(database_url: str):
    database = Database(database_url)
    await database.connect()
    await run_script(database, dirname + '/structure.sql')
    await database.disconnect()

async def run_script(database: Database, script_path: str):
    # Lecture du fichier seed.sql
    sql_script = Path(script_path).read_text()
    
    # Exécution du script SQL
    for statement in sql_script.split(';'):
        if statement.strip():
            await database.execute(statement)

if __name__ == "__main__":
    asyncio.run(seed('sqlite+aiosqlite:///example.db'))