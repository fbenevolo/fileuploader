from unittest.mock import AsyncMock

import pytest

from src.service import MetadataService


@pytest.fixture
def metadata_repository():
    repository = AsyncMock()
    return repository


@pytest.fixture
def metadata_service(metadata_repository):
    return MetadataService(metadata_repository=metadata_repository)
