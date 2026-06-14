import os

from src.services.file_services import FileService
from src.repository.storage.storage_repository import (
    LocalStorageRepository,
    S3StorageRepository,
)
from src.repository.metadata.file_metadata_repository import (
    SQLiteMetadataRepository,
    PostgreSQLMetadataRepository,
)
from src.db.connection import SQLiteDatabase, PostgreSQLDatabase

from src.core.config import (
    POSTGRES_HOST,
    POSTGRES_DATABASE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    FILES_DIR,
)

database = PostgreSQLDatabase(
    POSTGRES_HOST, POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT
)
metadata_repository = PostgreSQLMetadataRepository(database)
storage_repository = S3StorageRepository(
    os.getenv("BUCKET_NAME"),
    os.getenv("aws_access_key_id"),
    os.getenv("aws_secret_access_key"),
)
file_service = FileService(
    metadata_repository=metadata_repository, storage_repository=storage_repository
)
