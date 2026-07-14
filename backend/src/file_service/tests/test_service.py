import pytest

from src.service import FileService
from src.models import FileUploadInput
from src.core.exceptions import EmptyFileException

from mocks import FakeStorageRepository


@pytest.mark.asyncio
async def test_upload_generates_url():

    storage = FakeStorageRepository()

    service = FileService(storage_repository=storage)

    file_input = FileUploadInput(original_name="test.txt", extension=".txt", size=100)

    result = await service.upload_file_service(file_input)

    assert "upload_url" in result
    assert result["filename"].endswith(".txt")


@pytest.mark.asyncio
async def test_upload_file_with_size_zero():

    storage = FakeStorageRepository()

    service = FileService(storage_repository=storage)

    file_input = FileUploadInput(original_name="test.txt", extension=".txt", size=0)

    with pytest.raises(EmptyFileException) as _:
        await service.upload_file_service(file_input)
