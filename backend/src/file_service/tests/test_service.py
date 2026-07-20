from unittest.mock import patch

import pytest

from src.models import FileUploadInput
from src.core.exceptions import (
    EmptyFileException,
    FileHasNoExtension,
    FileTooLargeException,
    FileUploadException,
    S3StorageException,
)
from src.core.config import FILE_MAX_SIZE


@pytest.mark.asyncio
async def test_should_raise_empty_file_exception(service):
    file = FileUploadInput(
        original_name="test.txt",
        extension=".txt",
        size=0,
    )

    with pytest.raises(EmptyFileException, match="File is empty"):
        await service.generate_upload_url_service(file)


@pytest.mark.asyncio
async def test_should_raise_file_too_large_exception(service):
    file = FileUploadInput(
        original_name="test.txt",
        extension=".txt",
        size=FILE_MAX_SIZE + 1,
    )

    with pytest.raises(FileTooLargeException, match="File is too large"):
        await service.generate_upload_url_service(file)


@pytest.mark.asyncio
async def test_should_raise_file_has_no_extension_exception(service):
    file = FileUploadInput(
        original_name="test",
        extension="",
        size=100,
    )

    with pytest.raises(FileHasNoExtension, match="File has no extension"):
        await service.generate_upload_url_service(file)


@pytest.mark.asyncio
async def test_should_raise_file_upload_exception_when_storage_fails(
    service,
    storage_repository,
):
    file = FileUploadInput(
        original_name="test.txt",
        extension=".txt",
        size=100,
    )

    storage_repository.generate_upload_url.side_effect = S3StorageException(
        "S3 failure"
    )

    with patch(
        "src.service.uuid.uuid4",
        return_value="12345678-1234-1234-1234-123456789abc",
    ):
        with pytest.raises(
            FileUploadException,
            match="Unable to generate upload URL.",
        ):
            await service.generate_upload_url_service(file)

    storage_repository.generate_upload_url.assert_called_once_with(
        "12345678-1234-1234-1234-123456789abc.txt"
    )


@pytest.mark.asyncio
async def test_should_generate_upload_url_successfully(
    service,
    storage_repository,
):
    file = FileUploadInput(
        original_name="test.txt",
        extension=".txt",
        size=100,
    )

    storage_repository.generate_upload_url.return_value = (
        "https://bucket.s3.amazonaws.com/upload"
    )

    uuid_value = "12345678-1234-1234-1234-123456789abc"

    with patch(
        "src.service.uuid.uuid4",
        return_value=uuid_value,
    ):
        response = await service.generate_upload_url_service(file)

    storage_repository.generate_upload_url.assert_called_once_with(f"{uuid_value}.txt")

    assert response.file_id == uuid_value
    assert response.filename == f"{uuid_value}.txt"
    assert response.upload_url == "https://bucket.s3.amazonaws.com/upload"
