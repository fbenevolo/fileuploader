from src.services.file_services import FileService
from src.repository.storage.storage_repository import LocalStorageRepository
from src.repository.metadata.file_metadata_repository import SQLiteMetadataRepository, PostgreSQLMetadataRepository
from src.db.connection import SQLiteDatabase, PostgreSQLDatabase

from src.core.config import POSTGRES_HOST, POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, FILES_DIR

database = PostgreSQLDatabase(POSTGRES_HOST,
                              POSTGRES_DATABASE,
                              POSTGRES_USER,
                              POSTGRES_PASSWORD,
                              POSTGRES_PORT
                              )
metadata_repository = PostgreSQLMetadataRepository(database)
storage_repository = LocalStorageRepository(FILES_DIR)
file_service = FileService(
    metadata_repository=metadata_repository,
    storage_repository=storage_repository
)