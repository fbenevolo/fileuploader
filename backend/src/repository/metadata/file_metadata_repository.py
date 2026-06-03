import logging
from typing import List, Protocol

from src.models.file_models import FileModel
from src.db.connection import SQLiteDatabase

logger = logging.getLogger(__name__)

class MetadataRepository(Protocol):
    async def upload_metadata(self, file_object: FileModel) -> None: ...
    async def list_metadata(self) -> List[FileModel]: ...
    async def delete_metadata(self, stored_name: str) -> None: ...


class SQLiteMetadataRepository:
    def __init__(self, db_connection: SQLiteDatabase) -> List[FileModel]:
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
                        created_at=row[4]
                    ).model_dump()
                    for row in rows
                ]
            except Exception as e:
                logger.exception(f"Error retriveving files metadata: {e}")
                raise


    async def upload_metadata(self, file_object: FileModel) -> None:
        async with self.db_connection.get_connection() as connection:
            try:
                logger.info(f"Uploading file metadata {file_object.original_name} to storage")
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
                """, (
                    file_object.file_id,
                    file_object.original_name,
                    file_object.stored_name,
                    file_object.size,
                    file_object.created_at
                ))

                await connection.commit()
            except Exception as e:
                logger.exception(f"Error uploading file metadata {file_object.original_name}: {e}")
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
                """, (stored_name,)
                )

                await connection.commit()
                logging.info(f"Rows affected: {cursor.rowcount}")
            except Exception as e:
                logger.exception(f"Error deleting file metadata: {e}")
                raise