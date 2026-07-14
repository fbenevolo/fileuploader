import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.service import MetadataService
from src.core.exceptions import ModeNotFound


from src.repository import (
    PostgreSQLMetadataRepository,
    DynamoDBMetadataRepository,
)
from src.db.connection import PostgreSQLDatabase


def create_app(mode: str) -> FastAPI:
    if mode not in ("aws", "local"):
        raise ModeNotFound("mode must be 'aws' or 'local' ")

    database = None
    if mode == "aws":
        metadata_repository = DynamoDBMetadataRepository(os.getenv("DYNAMODB_TABLE"))
    else:
        database = PostgreSQLDatabase(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DATABASE"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=int(os.getenv("POSTGRES_PORT")),
        )
        metadata_repository = PostgreSQLMetadataRepository(database)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if database:
            await database.connect()
            await database.initialize()
            # setup_storage()
        yield
        if database:
            await database.disconnect()

    metadata_service = MetadataService(
        metadata_repository=metadata_repository,
    )
    app = FastAPI(lifespan=lifespan)
    app.state.metadata_service = metadata_service
    return app
