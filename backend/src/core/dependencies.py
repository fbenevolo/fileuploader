from src.services.file_services import FileService
from src.storage.storage import LocalStorageRepository
from src.repository.file_metadata_repository import LocalMetadataRepository
from src.db.connection import SQLiteDatabase

from src.core.config import DB_PATH, FILES_DIR

database = SQLiteDatabase(DB_PATH)
metadata_repository = LocalMetadataRepository(database)
storage_repository = LocalStorageRepository(FILES_DIR)
file_service = FileService(
    metadata_repository=metadata_repository,
    storage_repository=storage_repository
)