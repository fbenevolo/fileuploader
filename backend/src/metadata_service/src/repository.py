import aioboto3
import logging
from typing import List, Protocol
from botocore.exceptions import ClientError
from src.core.exceptions import DynamoDBException
from src.models import MetadataInput
from src.db.connection import PostgreSQLDatabase

logger = logging.getLogger(__name__)


class MetadataRepository(Protocol):
    async def upload_metadata(self, metadata_input: MetadataInput) -> None: ...
    async def list_metadata(self) -> List[MetadataInput]: ...
    async def delete_metadata(self, stored_name: str) -> None: ...


class PostgreSQLMetadataRepository:
    def __init__(self, db_connection: PostgreSQLDatabase):
        self.db_connection = db_connection

    async def upload_metadata(self, file_object: MetadataInput) -> None:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info(f"Uploading file metadata {file_object.original_name}")

                await connection.execute(
                    """
                    INSERT INTO files (
                        file_id,
                        original_name,
                        stored_name,
                        size,
                        created_at
                    )
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    file_object.file_id,
                    file_object.original_name,
                    file_object.stored_name,
                    file_object.size,
                    file_object.created_at,
                )
                logger.info("Metadata uploaded successfully")
            except Exception as e:
                raise Exception(
                    f"Error uploading file metadata {file_object.original_name}"
                ) from e

    async def list_metadata(self) -> List[dict]:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info("Retrieving files metadata")
                rows = await connection.fetch(
                    """
                    SELECT
                        file_id,
                        original_name,
                        stored_name,
                        size,
                        created_at
                    FROM files
                    """
                )
                logger.info("Metadata retrieved")
                return [
                    MetadataInput(
                        file_id=row["file_id"],
                        original_name=row["original_name"],
                        stored_name=row["stored_name"],
                        size=row["size"],
                        created_at=row["created_at"],
                    ).model_dump()
                    for row in rows
                ]
            except Exception as e:
                raise Exception(f"Error retrieving files metadata") from e

    async def delete_metadata(self, file_id: str) -> None:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info(f"Deleting metadata for file {file_id}")

                result = await connection.execute(
                    """
                    DELETE FROM files
                    WHERE stored_name = $1
                    """,
                    file_id,
                )

                logger.info(f"Deleted file: {result}")

            except Exception as e:
                raise Exception(f"Error deleting file metadata") from e


class DynamoDBMetadataRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.session = aioboto3.Session()

    async def upload_metadata(self, file_object: MetadataInput) -> None:
        try:
            async with self.session.client("dynamodb") as dynamo_client:
                await dynamo_client.put_item(
                    TableName=self.table_name,
                    Item={
                        "file_id": {"S": file_object.file_id},
                        "created_at": {"S": file_object.created_at},
                        "original_name": {"S": file_object.original_name},
                        "stored_name": {"S": file_object.stored_name},
                        "size": {"N": str(file_object.size)},
                    },
                )
        except ClientError as e:
            raise DynamoDBException(
                "Error occured during upload of metadata to AWS"
            ) from e

    async def list_metadata(self) -> List[MetadataInput]:
        try:
            async with self.session.client("dynamodb") as dynamo_client:
                response = await dynamo_client.scan(TableName=self.table_name)
                items = []
                for item in response["Items"]:
                    items.append(
                        MetadataInput(
                            file_id=item["file_id"]["S"],
                            created_at=item["created_at"]["S"],
                            original_name=item["original_name"]["S"],
                            stored_name=item["stored_name"]["S"],
                            size=int(item["size"]["N"]),
                        )
                    )

                return items
        except ClientError as e:
            raise DynamoDBException("Error occured during listing metadata") from e

    async def delete_metadata(self, stored_name: str) -> None:
        try:
            file_id = stored_name[:-4]
            async with self.session.client("dynamodb") as dynamo_client:
                await dynamo_client.delete_item(
                    TableName=self.table_name, Key={"file_id": {"S": file_id}}
                )
        except ClientError as e:
            raise DynamoDBException("Error occured deleting metadata") from e
