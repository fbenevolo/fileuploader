from pydantic import BaseModel
from datetime import datetime

class FileModel(BaseModel):
    file_id: str
    original_name: str
    stored_name: str
    size: int
    created_at: datetime

    def __eq__(self, other):
        return other.original_name == self.original_name


class FileUploadInput(BaseModel):
    original_name: str
    content: bytes
    extension: str
    size: int
