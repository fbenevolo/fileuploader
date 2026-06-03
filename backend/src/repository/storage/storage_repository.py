import logging
import aiofiles
import aiofiles.os
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)

class StorageRepository(Protocol):
    async def upload_file(self, file_content: bytes, filename: str) -> None: ...
    async def download_file(self, stored_name: str): ...
    async def delete_file(self, stored_name: str) -> None: ...


class LocalStorageRepository:
    def __init__(self, files_dir: Path):
        self.files_dir = files_dir

    async def upload_file(self, file_content, filename):
        stored_path = self.files_dir / filename
        async with aiofiles.open(stored_path, "wb") as out_file:
            try:
                logger.info(f"Uploading file {filename} to storage")
                await out_file.write(file_content)
            except Exception as e:
                logger.exception(f"Error uploading file {filename}: {e}")
                raise
    
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


class S3StorageRepository:
    def __init__(self, files_dir: Path):
        self.files_dir = files_dir

    async def upload_file(self, file_content: bytes, filename: str) -> None:
        ... 

    async def download_file(self, stored_name: str):
        ...

    async def delete_file(self, stored_name: str) -> None:
        ...