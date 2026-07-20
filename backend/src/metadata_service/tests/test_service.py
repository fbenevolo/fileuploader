import pytest


@pytest.mark.asyncio
async def test_should_return_metadata_list(
    metadata_service,
    metadata_repository,
):
    expected_rows = [
        {
            "file_id": "123",
            "filename": "test.txt",
        },
        {
            "file_id": "456",
            "filename": "image.png",
        },
    ]

    metadata_repository.list_metadata.return_value = expected_rows

    result = await metadata_service.list_metadata_service()

    assert result == expected_rows

    metadata_repository.list_metadata.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_should_upload_metadata(
    metadata_service,
    metadata_repository,
):
    event = {
        "file_id": "123",
        "filename": "test.txt",
        "size": 1024,
    }

    await metadata_service.upload_metadata_service(event)

    metadata_repository.upload_metadata.assert_awaited_once_with(event)


@pytest.mark.asyncio
async def test_should_delete_metadata(
    metadata_service,
    metadata_repository,
):
    file_id = "123456"

    await metadata_service.delete_metadata_service(file_id)

    metadata_repository.delete_metadata.assert_awaited_once_with(file_id)
