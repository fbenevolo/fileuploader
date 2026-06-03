import pytest

@pytest.mark.asyncio
async def test_upload_file(file_service_fixture, file_input, file_object):
    object = await file_service_fixture.upload_file_service(file_input)
    assert object == file_object


@pytest.mark.asyncio
async def test_list_files(file_service_fixture, file_object):
    objects = await file_service_fixture.list_files_metadata_service()

    assert objects[0]["original_name"] == file_object.original_name