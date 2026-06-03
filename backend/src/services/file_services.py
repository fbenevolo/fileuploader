import uuid
import logging
from datetime import datetime

from src.storage.storage import StorageRepository
from src.repository.file_metadata_repository import LocalMetadataRepository
from src.models.file_models import FileModel, FileUploadInput

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self, metadata_repository: LocalMetadataRepository, storage_repository: StorageRepository):
        self.metadata_repository = metadata_repository
        self.storage_repository = storage_repository

    async def list_files_metadata_service(self):
        try:
            rows = await self.metadata_repository.list_metadata()
            return [
                FileModel(
                    file_id=row[0],
                    original_name=row[1],
                    stored_name=row[2],
                    size=row[3],
                    created_at=row[4]
                ).model_dump()
                for row in rows
            ]
        except Exception as e:
            raise


    async def upload_file_service(self, file_input: FileUploadInput):
        # TODO escrever checagens

        # gera metadados
        new_uuid = str(uuid.uuid4())
        file_object = FileModel(
            file_id=new_uuid,
            original_name=file_input.original_name,
            stored_name=f"{new_uuid}.{file_input.extension}",
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

            raise

        return file_object

    async def download_file_service(self, stored_name: str):
        await self.storage_repository.download_file(stored_name)

    async def delete_file_service(self, stored_name):
        try:
            await self.storage_repository.delete_file(stored_name)
            await self.metadata_repository.delete_metadata(stored_name)
        except Exception as e:
            raise e 