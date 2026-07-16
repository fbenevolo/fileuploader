import logging
from typing import Any

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

    async def upload_metadata_service(self, event: Any):
        await self.metadata_repository.upload_metadata(event)

    async def delete_metadata_service(self, file_id: str):
        await self.metadata_repository.delete_metadata(file_id)
