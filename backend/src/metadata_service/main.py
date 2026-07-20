import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

import os
from dotenv import load_dotenv
import uvicorn
from mangum import Mangum
from src.routes import router
from src.core.factory import create_app

load_dotenv()

logger = logging.getLogger(__name__)

app = create_app(os.getenv("APP_MODE"))
app.include_router(router)

handler = Mangum(app)

# local execution
if __name__ == "__main__":
    try:
        logger.info(f"Server running on port {os.getenv('PORT')}")
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT")))
    except Exception as e:
        logger.error(f"Error running server: {e}")
