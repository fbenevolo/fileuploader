from pathlib import Path

import pytest
import pytest_asyncio

from src.core.config import BASE_DIR
from src.db.connection import SQLiteDatabase
from src.models.file_models import FileModel, FileUploadInput

from src.repository.file_metadata_repository import LocalMetadataRepository



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


from src.services.file_services import FileService
from src.storage.storage import LocalStorageRepository


@pytest_asyncio.fixture
async def database_fixture(tmp_path):
    db_path  = tmp_path / "test.db"
    database = SQLiteDatabase(db_path)

    async with database.get_connection() as connection:
        with open("scripts/create_file_metadata_table.sql") as query:
            sql = query.read()
        await connection.execute(sql)
        await connection.commit()

        with open("scripts/create_sample_metadata.sql") as query:
            sql = query.read()
        await connection.execute(sql)
        await connection.commit()

    return database

@pytest_asyncio.fixture
def local_metadata_repository_fixture(database_fixture) -> LocalMetadataRepository:
    return LocalMetadataRepository(database_fixture)

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
