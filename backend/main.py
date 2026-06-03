from fastapi import FastAPI
import logging
import uvicorn

from src.routes.file_routes import router
from src.db.init import setup_database
from src.core.config import setup_storage

PORT = 5000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    try:
        setup_storage()
        setup_database()
        uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
        logger.info(f"Server running on port {PORT}")
    except Exception as e:
        logger.error(f"Error running server: {e}")