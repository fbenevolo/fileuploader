from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FILES_DIR = DATA_DIR / "files"
DB_PATH = DATA_DIR / "database.db"

FILE_MAX_SIZE = 50000


def setup_storage():
    DATA_DIR.mkdir(exist_ok=True)
    FILES_DIR.mkdir(exist_ok=True)
