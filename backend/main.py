from mangum import Mangum
import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routes.file_routes import router
from src.core.config import setup_storage
from src.core.dependencies import database

PORT = 5000

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    setup_storage()
    await database.connect()
    await database.initialize()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

handler = Mangum(app)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
        logger.info(f"Server running on port {PORT}")
    except Exception as e:
        logger.error(f"Error running server: {e}")
