import pytest
import aiosqlite
from src.models.file_models import FileModel, FileUploadInput

@pytest.fixture
def file_input():
    return FileUploadInput(
        original_name="123.txt",
        content=b"Greetings",
        extension="txt",
        size=100
    )


@pytest.fixture
def file_object(file_input):
    file_id = "123456"
    return FileModel(
        file_id=file_id,
        original_name=file_input.original_name,
        stored_name=f"{file_id}{file_input.extension}",
        size=file_input.size,
        created_at="2026-05-30"
    )