from pydantic import BaseModel


class MetadataInput(BaseModel):
    file_id: str
    original_name: str
    stored_name: str
    size: int
    created_at: str

    def __eq__(self, other):
        return other.original_name == self.original_name
