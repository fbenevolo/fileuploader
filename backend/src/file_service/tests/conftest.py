from unittest.mock import AsyncMock, Mock

import pytest

from src.service import FileService


@pytest.fixture
def storage_repository():
    repository = Mock()

    repository.save_file = AsyncMock()
    repository.download_file = AsyncMock()
    repository.delete_file = AsyncMock()
    repository.generate_upload_url = Mock()

    return repository


@pytest.fixture
def metadata_publisher():
    publisher = Mock()
    publisher.publish = AsyncMock()
    return publisher


@pytest.fixture
def service(storage_repository, metadata_publisher):
    return FileService(
        storage_repository=storage_repository,
        metadata_publisher=metadata_publisher,
    )
