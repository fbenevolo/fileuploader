import uuid
import logging

from src.models import FileUploadInput, UploadUrlResponse, FileUploadedEvent
from src.core.config import FILE_MAX_SIZE
from src.core.exceptions import (
    EmptyFileException,
    FileHasNoExtension,
    FileTooLargeException,
    FileUploadException,
    S3StorageException,
)
from src.repository import StorageRepository
from src.producer import MetadataPublisher

logger = logging.getLogger(__name__)


class FileService:
    def __init__(
        self,
        storage_repository: StorageRepository,
        metadata_publisher: MetadataPublisher,
    ):
        self.storage_repository = storage_repository
        self.metadata_publisher = metadata_publisher

    async def save_file_service(self, metadata: FileUploadedEvent, content: bytes):
        await self.storage_repository.save_file(metadata.stored_name, content)
        await self.metadata_publisher.publish(metadata)

    async def generate_upload_url_service(
        self, file_input: FileUploadInput
    ) -> UploadUrlResponse:
        if file_input.size == 0:
            raise EmptyFileException("File is empty")
        if file_input.size > FILE_MAX_SIZE:
            raise FileTooLargeException("File is too large")
        if file_input.extension == "":
            raise FileHasNoExtension("File has no extension")

        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_input.extension}"

        try:
            upload_url = self.storage_repository.generate_upload_url(filename)
            return UploadUrlResponse(
                file_id=file_id, filename=filename, upload_url=upload_url
            )
        except S3StorageException as e:
            raise FileUploadException("Unable to generate upload URL.") from e

    async def download_file_service(self, stored_name: str):
        return await self.storage_repository.download_file(stored_name)

    async def delete_file_service(self, stored_name):
        await self.storage_repository.delete_file(stored_name)
