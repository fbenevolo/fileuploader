import shutil
import logging
import aiofiles
from pathlib import Path
from typing import Protocol

from src.core.config import FILES_DIR

logger = logging.getLogger(__name__)

class StorageRepository(Protocol):
    async def upload_file(self, file_content: bytes, filename: str) -> None:
        ...

    async def download_file(self, stored_name: str):
        ...

    async def delete_file(self, stored_name: str) -> None:
        ...

class LocalStorageRepository:
    async def upload_file(self, file_content, filename):
        stored_path = FILES_DIR / filename
        async with aiofiles.open(stored_path, "wb") as out_file:
            try:
                logger.info(f"Uploading file {filename} to storage")
                await out_file.write(file_content)
            except Exception as e:
                logger.exception(f"Error uploading file {filename}: {e}")
                raise
    
    async def download_file(self, stored_name):
        filepath = FILES_DIR / stored_name
        if not filepath.exists():
            logging.exception(f"Requested file {stored_name} does not exist")
            raise FileNotFoundError(f"Requested file {stored_name} does not exist")
        
        downloads_dir = Path.home() / "Downloads"
        downloads_dir.mkdir(exist_ok=True)
        dest = downloads_dir / stored_name
        shutil.copy2(filepath, dest)
    
        logger.info(f"File {stored_name} downloaded to {dest}")

    async def delete_file(self, stored_name):
        filepath = FILES_DIR / stored_name
        if filepath.exists():
            logger.info(f"Deleting file {stored_name}")
            try:
                await aiofiles.remove(filepath)
                logger.info(f"File deleted successfully")
            except Exception as e:
                logger.exception(f"Could not delete file {stored_name}: {e}")
                raise


class S3StorageRepository:
    async def upload_file(self, file_content: bytes, filename: str) -> None:
        ... 

    async def download_file(self, stored_name: str):
        ...

    async def delete_file(self, stored_name: str) -> None:
        ...