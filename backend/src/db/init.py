import logging
import sqlite3
from pathlib import Path
from src.core.config import DATA_DIR, FILES_DIR, DB_PATH

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent


def setup_database():
    if not DATA_DIR.exists():
        logger.info("Creating storage folder...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not FILES_DIR.exists():
        logger.info("Creating files folder...")
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    # PRIMEIRO BLOCO
    with (
        sqlite3.connect(DB_PATH) as connection,
        open(BASE_DIR / "create_file_table.sql") as schema,
    ):
        logger.info("Creating table files...")
        cursor = connection.cursor()
        cursor.executescript(schema.read())
        connection.commit()
        logger.info("Table created successfully")

    logger.info("Database setup complete")
