import os
import pika
import logging
from src.models import FileUploadedEvent

logger = logging.getLogger(__name__)


class MetadataPublisher:
    async def publish(self, metadata: FileUploadedEvent):
        raise NotImplementedError


class RabbitMQMetadataPublisher(MetadataPublisher):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name

    async def publish(self, metadata: FileUploadedEvent):
        logger.info("Received metadata")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"))
        )
        with connection.channel() as channel:
            channel.queue_declare(
                queue=self.queue_name,
                durable=True,
                arguments={"x-queue-type": "quorum"},
            )
            channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=metadata.model_dump_json(),
            )

            logging.info("Metadata published by producer")

        connection.close()
