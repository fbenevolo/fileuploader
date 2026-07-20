import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# sqs_handler.py

import json

from src.service import MetadataService
from src.repository import MetadataRepository


repository = MetadataRepository()
service = MetadataService(repository)


def handler(event, context):
    print(json.dumps(event))

    # for record in event["Records"]:

    #     body = json.loads(record["body"])

    #     event_type = body["event_type"]

    #     if event_type == "FILE_CREATED":
    #         service.upload_metadata(body)

    #     elif event_type == "FILE_DELETED":
    #         service.delete_metadata(body)

    # return {
    #     "statusCode": 200
    # }
