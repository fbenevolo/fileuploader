import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
FILES_DIR = DATA_DIR / "files"
DB_PATH = DATA_DIR / "database.db"

FILE_MAX_SIZE = 5000

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "fileuploader")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))


def setup_storage():
    DATA_DIR.mkdir(exist_ok=True)
    FILES_DIR.mkdir(exist_ok=True)
