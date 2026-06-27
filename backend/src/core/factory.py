import os
from typing import Optional
from fastapi import FastAPI
from dataclasses import dataclass
from contextlib import asynccontextmanager
from src.core.exceptions import ModeNotFound


from src.services.file_services import FileService
from src.repository.storage.storage_repository import (
    LocalStorageRepository,
    S3StorageRepository,
)
from src.repository.metadata.file_metadata_repository import (
    PostgreSQLMetadataRepository,
    DynamoDBMetadataRepository,
)
from src.db.connection import PostgreSQLDatabase

from src.core.config import (
    POSTGRES_HOST,
    POSTGRES_DATABASE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    FILES_DIR,
    setup_storage,
)


@dataclass
class AppStack:
    metadata_repository: object
    storage_repository: object
    database: Optional[object] = None


class AWSProvider:
    @classmethod
    def build_stack(cls):
        metadata_repository = DynamoDBMetadataRepository(
            os.getenv("DYNAMO_TABLE"),
        )
        storage_repository = S3StorageRepository(
            os.getenv("BUCKET_NAME"),
        )

        return AppStack(metadata_repository, storage_repository, None)


class LocalProvider:
    @classmethod
    def build_stack(cls):
        database = PostgreSQLDatabase(
            POSTGRES_HOST,
            POSTGRES_DATABASE,
            POSTGRES_USER,
            POSTGRES_PASSWORD,
            POSTGRES_PORT,
        )
        metadata_repository = PostgreSQLMetadataRepository(database)
        storage_repository = LocalStorageRepository(FILES_DIR)
        return AppStack(metadata_repository, storage_repository, database)


def create_app(mode: str) -> FastAPI:
    if mode not in ("aws", "local"):
        raise ModeNotFound("mode must be 'aws' or 'local' ")

    if mode == "aws":
        stack = AWSProvider.build_stack()
    else:
        stack = LocalProvider.build_stack()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if stack.database:
            await stack.database.connect()
            await stack.database.initialize()
            setup_storage()
        yield
        if stack.database:
            await stack.database.disconnect()

    file_service = FileService(
        metadata_repository=stack.metadata_repository,
        storage_repository=stack.storage_repository,
    )
    app = FastAPI(lifespan=lifespan)
    app.state.file_service = file_service
    return app
