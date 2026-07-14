class FakeStorageRepository:
    def __init__(self):
        self.files = {}

    async def upload_file(self, filename: str) -> str:
        url = f"https://fake-s3.com/{filename}"
        self.files[filename] = {"url": url}
        return url

    async def download_file(self, filename: str) -> str:
        if filename not in self.files:
            raise FileNotFoundError()

        return self.files[filename]["url"]

    async def delete_file(self, filename: str):
        if filename not in self.files:
            raise FileNotFoundError()

        del self.files[filename]
