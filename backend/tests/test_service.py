import pytest
from src.services.file_services import upload_file_service


@pytest.mark.asyncio
async def test_upload_file(file_input, file_object):
    object = await upload_file_service(file_input)
    assert object == file_object