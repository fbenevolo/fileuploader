import aiosqlite
from pathlib import Path
from typing import AsyncIterator
from contextlib import asynccontextmanager

class SQLiteDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        async with aiosqlite.connect(self.db_path) as connection:
            connection.row_factory = aiosqlite.Row
            yield connection