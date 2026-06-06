import os
import boto3
import logging
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".backend-env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)


logger = logging.getLogger(__name__)

def populate_s3():
    client = boto3.client("s3",
                          aws_access_key_id=os.getenv("aws_access_key_id"),
                          aws_secret_access_key=os.getenv("aws_secret_access_key"))
    
    logger.info("Populating s3 with sample files...")
    samples_dir  = Path(__file__).resolve().parent / "samples"
    for file in samples_dir.iterdir():
        with open(file, "r") as f:
            client.put_object(
                Bucket=os.getenv("BUCKET_NAME"),
                Body=f.read(),
                Key=file.name
            )

    logger.info("Populated s3 successfully")

def populate_dynamo():
    client = boto3.resource("dynamodb",
                          aws_access_key_id=os.getenv("aws_access_key_id"),
                          aws_secret_access_key=os.getenv("aws_secret_access_key"),
                          region_name=os.getenv("REGION_NAME"))

    logger.info("Populating dynamo with sample files metadata")

    table = client.Table(os.getenv("DYNAMO_TABLE"))

    table.put_item(
        Item={
        "file_id": "123",
        "original_name": "first_file.txt",
        "stored_name": "123.txt",
        "size": 100,
        "created_at": "2026-06-06"
    })

    table.put_item(
        Item={
        "file_id": "456",
        "original_name": "second_file.txt",
        "stored_name": "456.txt",
        "size": 200,
        "created_at": "2026-06-06"
    })


    logger.info("Dynamo populated successfully")

if __name__ == "__main__":
    populate_s3()
    populate_dynamo()