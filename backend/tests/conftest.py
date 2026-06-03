from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from pathlib import Path

from src.db.connection import SQLiteDatabase
from src.models.file_models import FileModel, FileUploadInput
from src.repository.metadata.file_metadata_repository import SQLiteMetadataRepository
from src.services.file_services import FileService
from src.repository.storage.storage_repository import LocalStorageRepository



@pytest.fixture
def file_input():
    return FileUploadInput(
        original_name="123.txt",
        content=b"Greetings",
        extension="txt",
        size=100
    )


@pytest.fixture
def file_object(file_input):
    file_id = "123456"
    return FileModel(
        file_id=file_id,
        original_name=file_input.original_name,
        stored_name=f"{file_id}{file_input.extension}",
        size=file_input.size,
        created_at="2026-05-30"
    )

@pytest_asyncio.fixture
async def database_fixture(tmp_path):
    db_path  = tmp_path / "test.db"
    database = SQLiteDatabase(db_path)

    async with database.get_connection() as connection:
        with open("scripts/create_file_metadata_table.sql") as query:
            sql = query.read()
        await connection.execute(sql)
        await connection.commit()

    return database

@pytest_asyncio.fixture
async def populate_database_fixture(database_fixture):
    async with database_fixture.get_connection() as connection:
        with open("scripts/create_sample_metadata.sql") as query:
            sql = query.read()
        await connection.execute(sql)
        await connection.commit()
    
    return database_fixture

@pytest_asyncio.fixture
def local_metadata_repository_fixture(database_fixture) -> SQLiteMetadataRepository:
    return SQLiteMetadataRepository(database_fixture)

@pytest_asyncio.fixture
def local_storage_repository_fixture(tmp_path) -> LocalStorageRepository:
    files_dir = tmp_path / "files/"
    files_dir.mkdir(parents=True, exist_ok=True)
    return LocalStorageRepository(files_dir)

@pytest_asyncio.fixture
def file_service_fixture(local_metadata_repository_fixture, local_storage_repository_fixture) -> FileService:
    return FileService(
        local_metadata_repository_fixture,
        local_storage_repository_fixture
    )

@pytest.fixture
def file_service_with_metadata_failure():
    storage = AsyncMock()
    storage.upload_file.return_value = None

    metadata = AsyncMock()
    metadata.upload_metadata.side_effect = Exception("Metadata failure")
    return FileService(metadata, storage)

@pytest.fixture
def file_service_with_file_failure():
    storage = AsyncMock()
    storage.upload_file.return_value = None
    storage.upload_file.side_effect = Exception("File failure")
    metadata = AsyncMock()
    return FileService(metadata, storage)
