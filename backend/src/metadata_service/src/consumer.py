import os
import aio_pika
import logging
import asyncio

from src.models import MetadataInput
from src.service import MetadataService

logger = logging.getLogger(__name__)


class MetadataConsumer:
    def __init__(self, queue_name: str, metadata_service: MetadataService):
        self.queue_name = queue_name
        self.metadata_service = metadata_service

    async def start(self):

        connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_CONNECTION_URL"))

        channel = await connection.channel()
        queue = await channel.declare_queue(
            self.queue_name, durable=True, arguments={"x-queue-type": "quorum"}
        )

        await queue.consume(self.process)

        await asyncio.Future()  # mantém o consumer vivo

    async def process(self, message: aio_pika.IncomingMessage):
        async with message.process():
            logger.info("Metadata received by consumer")
            event = MetadataInput.model_validate_json(message.body)
            await self.metadata_service.upload_metadata_service(event)
