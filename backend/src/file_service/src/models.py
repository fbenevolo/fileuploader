from pydantic import BaseModel


class FileUploadInput(BaseModel):
    original_name: str
    extension: str
    size: int


class UploadUrlResponse(BaseModel):
    file_id: str
    filename: str
    upload_url: str
