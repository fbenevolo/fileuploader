import logging
import uvicorn
from mangum import Mangum
from src.routes.file_routes import router
from src.core.factory import create_app

PORT = 5000

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


app = create_app("aws")
app.include_router(router)

handler = Mangum(app)

if __name__ == "__main__":
    try:
        app = create_app("local")
        uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
        logger.info(f"Server running on port {PORT}")
    except Exception as e:
        logger.error(f"Error running server: {e}")
