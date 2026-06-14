import aiosqlite
import asyncpg
from pathlib import Path
from typing import AsyncIterator, Protocol
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection(Protocol):
    async def get_connection(self): ...


class SQLiteDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    async def initialize(self):
        logger.info("Creating database table...")
        async with self.get_connection() as connection:
            sql = (Path(__file__).parent / "create_file_table.sql").read_text()
            await connection.execute(sql)
        logger.info("Table files created successfully")

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        async with aiosqlite.connect(self.db_path) as connection:
            connection.row_factory = aiosqlite.Row
            yield connection


class PostgreSQLDatabase:
    def __init__(self, host: str, database: str, user: str, password: str, port: int):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.pool = None

    async def initialize(self):
        if self.pool is None:
            raise RuntimeError("Database pool not initialized. Call connect() first.")

        logger.info("Creating database table...")
        async with self.get_connection() as connection:
            sql = (Path(__file__).parent / "create_file_table.sql").read_text()
            await connection.execute(sql)
        logger.info("Table files created successfully")

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
            min_size=1,
            max_size=10,
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def get_connection(self):
        connection = await self.pool.acquire()
        try:
            yield connection
        finally:
            await self.pool.release(connection)
