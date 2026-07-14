import logging

from src.models import MetadataInput
from src.core.exceptions import DynamoDBException, MetadataUploadException
from src.repository import MetadataRepository

logger = logging.getLogger(__name__)


class MetadataService:
    def __init__(
        self,
        metadata_repository: MetadataRepository,
    ):
        self.metadata_repository = metadata_repository

    async def list_metadata_service(self):
        rows = await self.metadata_repository.list_metadata()
        return rows

    async def upload_metadata_service(self, metadata_input: MetadataInput):
        try:
            await self.metadata_repository.upload_metadata(metadata_input)
        except DynamoDBException as e:
            raise MetadataUploadException("Error uploading metadata") from e
        except Exception as e2:
            raise e2

    async def delete_metadata_service(self, file_id: str):
        await self.metadata_repository.delete_metadata(file_id)
