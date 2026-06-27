import datetime

import aioboto3
import logging
from typing import List, Protocol

from src.models.file_models import FileModel
from src.db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class MetadataRepository(Protocol):
    async def upload_metadata(self, file_object: FileModel) -> None: ...
    async def list_metadata(self) -> List[FileModel]: ...
    async def delete_metadata(self, stored_name: str) -> None: ...


class SQLiteMetadataRepository:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def list_metadata(self):
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info("Retrieving files metadata from storage")
                cursor = await connection.cursor()
                await cursor.execute("SELECT * FROM files")
                logger.info("Metadata retrieved")
                rows = await cursor.fetchall()
                return [
                    FileModel(
                        file_id=row[0],
                        original_name=row[1],
                        stored_name=row[2],
                        size=row[3],
                        created_at=row[4],
                    ).model_dump()
                    for row in rows
                ]
            except Exception as e:
                logger.exception(f"Error retriveving files metadata: {e}")
                raise

    async def upload_metadata(self, file_object: FileModel) -> None:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info(
                    f"Uploading file metadata {file_object.original_name} to storage"
                )
                cursor = await connection.cursor()
                await cursor.execute(
                    """
                    INSERT INTO files (
                        file_id,
                        original_name,
                        stored_name,
                        size,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        file_object.file_id,
                        file_object.original_name,
                        file_object.stored_name,
                        file_object.size,
                        file_object.created_at,
                    ),
                )

                await connection.commit()
            except Exception as e:
                logger.exception(
                    f"Error uploading file metadata {file_object.original_name}: {e}"
                )
                raise

    async def delete_metadata(self, stored_name: str) -> None:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info(f"Deleting file metadata")
                cursor = await connection.cursor()
                await cursor.execute(
                    """
                    DELETE FROM files
                    WHERE stored_name = ?
                """,
                    (stored_name,),
                )

                await connection.commit()
                logging.info(f"Rows affected: {cursor.rowcount}")
            except Exception as e:
                logger.exception(f"Error deleting file metadata: {e}")
                raise


class PostgreSQLMetadataRepository:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def upload_metadata(self, file_object: FileModel) -> None:
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

            except Exception as e:
                logger.exception(
                    f"Error uploading file metadata {file_object.original_name}: {e}"
                )
                raise

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
                    FileModel(
                        file_id=row["file_id"],
                        original_name=row["original_name"],
                        stored_name=row["stored_name"],
                        size=row["size"],
                        created_at=row["created_at"],
                    ).model_dump()
                    for row in rows
                ]
            except Exception as e:
                logger.exception(f"Error retrieving files metadata: {e}")
                raise

    async def delete_metadata(self, stored_name: str) -> None:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info(f"Deleting metadata for file {stored_name}")

                result = await connection.execute(
                    """
                    DELETE FROM files
                    WHERE stored_name = $1
                    """,
                    stored_name,
                )

                logger.info(result)

            except Exception as e:
                logger.exception(f"Error deleting file metadata: {e}")
                raise


class DynamoDBMetadataRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def get_session(self):
        return aioboto3.Session()

    async def upload_metadata(self, file_object: FileModel) -> None:
        try:
            async with self.get_session().client("dynamodb") as dynamo_client:
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
                logger.info("Uploaded file to dynamo successfully")
        except Exception as e:
            logger.error(f"Error occured during upload of metadata to AWS: {e}")
            raise

    async def list_metadata(self) -> List[FileModel]:
        try:
            async with self.get_session().client("dynamodb") as dynamo_client:
                response = await dynamo_client.scan(TableName=self.table_name)

                items = []

                for item in response["Items"]:
                    items.append(
                        FileModel(
                            file_id=item["file_id"]["S"],
                            created_at=item["created_at"]["S"],
                            original_name=item["original_name"]["S"],
                            stored_name=item["stored_name"]["S"],
                            size=int(item["size"]["N"]),
                        )
                    )

                return items
        except Exception as e:
            logger.error(f"Error occured during listing metadata: {e}")
            raise

    async def delete_metadata(self, file_id: str) -> None:
        try:
            async with self.get_session().client("dynamodb") as dynamo_client:
                await dynamo_client.delete_item(
                    TableName=self.table_name, Key={"file_id": {"S": file_id}}
                )
                logging.info("Item deleted successfully")
        except Exception as e:
            logger.error(f"Error occured deleting metadata: {e}")
            raise
