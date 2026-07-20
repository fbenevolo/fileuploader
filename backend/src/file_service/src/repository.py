import aioboto3
import logging
import aiofiles
import aiofiles.os
from pathlib import Path
from botocore.exceptions import BotoCoreError, ClientError
from src.core.exceptions import S3StorageException


logger = logging.getLogger(__name__)


class StorageRepository:
    async def generate_upload_url(self, filename: str) -> str:
        raise NotImplementedError

    async def download_file(self, file_id: str) -> bytes:
        raise NotImplementedError

    async def delete_file(self, file_id: str) -> None:
        raise NotImplementedError


class LocalStorageRepository(StorageRepository):
    def __init__(self, files_dir: Path):
        self.files_dir = files_dir

    def generate_upload_url(self, filename: str) -> str:
        return f"/files/upload/{filename}"

    async def download_file(self, stored_name: str) -> bytes:
        filepath = self.files_dir / stored_name
        if not filepath.exists():
            logging.exception(f"Requested file {stored_name} does not exist")
            raise FileNotFoundError(f"Requested file {stored_name} does not exist")
        async with aiofiles.open(filepath, "rb") as f:
            return await f.read()

    async def delete_file(self, stored_name):
        filepath = self.files_dir / stored_name
        if filepath.exists():
            logger.info(f"Deleting file {stored_name}")
            try:
                await aiofiles.os.remove(filepath)
                logger.info(f"File deleted successfully")
            except Exception as e:
                logger.exception(f"Could not delete file {stored_name}: {e}")
                raise
        else:
            logger.error("File not found")
            raise FileNotFoundError("File not found")

    async def save_file(self, filename: str, content: bytes) -> None:
        filepath = self.files_dir / filename
        try:
            async with aiofiles.open(filepath, "wb") as f:
                await f.write(content)
            logger.info(f"File {filename} saved successfully")
        except Exception as e:
            raise Exception(f"Could not save file {filename}") from e


class S3StorageRepository:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.session = aioboto3.Session()

    async def generate_upload_url(self, filename: str) -> str:
        """
        Instead of uploading the file, generates a presigned URL so that the client
        can directly upload the file to S3 through PUT method
        """
        try:
            async with self.session.client("s3") as s3_client:
                return await s3_client.generate_presigned_url(
                    ClientMethod="put_object",
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": filename,
                    },
                    ExpiresIn=3600,
                )
        except (BotoCoreError, ClientError) as e:
            raise S3StorageException(
                f"Error occured during upload of file {filename} to bucket {self.bucket_name}"
            ) from e

    async def download_file(self, stored_name: str) -> str:
        try:
            async with self.session.client("s3") as s3_client:
                return s3_client.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={"Bucket": self.bucket_name, "Key": stored_name},
                )
        except (BotoCoreError, ClientError) as e:
            raise S3StorageException(
                f"Error occured during download of file {stored_name}"
            ) from e

    async def delete_file(self, stored_name: str) -> None:
        try:
            async with self.session.client("s3") as s3_client:
                await s3_client.delete_object(Bucket=self.bucket_name, Key=stored_name)
        except (BotoCoreError, ClientError) as e:
            raise S3StorageException(
                f"Error occured during deletion of file {stored_name}"
            ) from e
