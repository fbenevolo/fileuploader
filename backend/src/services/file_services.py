import uuid
import logging
from datetime import datetime

from src.models.file_models import FileModel, FileUploadInput
from src.core.config import FILE_MAX_SIZE
from src.core.exceptions import EmptyFileException, FileHasNoExtension, FileTooLargeException
from src.repository.storage.storage_repository import StorageRepository
from src.repository.metadata.file_metadata_repository import SQLiteMetadataRepository

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self, metadata_repository: SQLiteMetadataRepository, storage_repository: StorageRepository):
        self.metadata_repository = metadata_repository
        self.storage_repository = storage_repository

    async def list_files_metadata_service(self):
        try:
            rows = await self.metadata_repository.list_metadata()
            return rows
        except Exception as e:
            raise


    async def upload_file_service(self, file_input: FileUploadInput):
        if file_input.size == 0:
            raise EmptyFileException("File is empty")
        if file_input.size > FILE_MAX_SIZE:
            raise FileTooLargeException("File is too large")
        if file_input.extension == "":
            raise FileHasNoExtension("File has no extension")

        # gera metadados
        new_uuid = str(uuid.uuid4())
        file_object = FileModel(
            file_id=new_uuid,
            original_name=file_input.original_name,
            stored_name=f"{new_uuid}{file_input.extension}",
            size=file_input.size,
            created_at=datetime.now().date()
        )

        file_uploaded = False
        metadata_uploaded = False

        try:
            await self.storage_repository.upload_file(file_input.content, file_object.stored_name)
            file_uploaded = True
            await self.metadata_repository.upload_metadata(file_object)
            metadata_uploaded = True
        except Exception as e:
            logger.exception(f"Some error occured while uploading file and metadata: {e}, Trying to rollback...")
            if file_uploaded:
                await self.storage_repository.delete_file(file_object.stored_name)
            if metadata_uploaded:
                await self.metadata_repository.delete_metadata(file_object.file_id)

            raise e

        return file_object

    async def download_file_service(self, stored_name: str):
        return await self.storage_repository.download_file(stored_name)

    async def delete_file_service(self, stored_name):
        try:
            await self.storage_repository.delete_file(stored_name)
            await self.metadata_repository.delete_metadata(stored_name)
        except Exception as e:
            raise e