from contextlib import asynccontextmanager
import aiosqlite
from src.core.config import DB_PATH

class SQLiteDatabase:
    @asynccontextmanager
    async def get_connection(self, db_path=DB_PATH):
        async with aiosqlite.connect(db_path) as connection:
            yield connection