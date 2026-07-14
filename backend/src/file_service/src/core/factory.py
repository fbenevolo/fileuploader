import os
import logging
from fastapi import FastAPI
from src.core.config import FILES_DIR
from src.core.exceptions import ModeNotFound


from src.service import FileService
from src.repository import (
    LocalStorageRepository,
    S3StorageRepository,
)

logger = logging.getLogger(__name__)


def create_app(mode: str) -> FastAPI:
    if mode not in ("aws", "local"):
        raise ModeNotFound("mode must be 'aws' or 'local' ")

    logger.info(f"Inicialing with mode {mode}")

    if mode == "aws":
        storage_repository = S3StorageRepository(os.getenv("BUCKET_NAME"))
    else:
        storage_repository = LocalStorageRepository(FILES_DIR)

    file_service = FileService(
        storage_repository=storage_repository,
    )
    app = FastAPI()
    app.state.file_service = file_service
    return app
