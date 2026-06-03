from src.services.file_services import FileService
from src.repository.storage.storage_repository import LocalStorageRepository
from src.repository.metadata.file_metadata_repository import SQLiteMetadataRepository
from src.db.connection import SQLiteDatabase

from src.core.config import DB_PATH, FILES_DIR

database = SQLiteDatabase(DB_PATH)
metadata_repository = SQLiteMetadataRepository(database)
storage_repository = LocalStorageRepository(FILES_DIR)
file_service = FileService(
    metadata_repository=metadata_repository,
    storage_repository=storage_repository
)