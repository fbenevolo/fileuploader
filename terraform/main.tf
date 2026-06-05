provider "aws" {
    region = var.region_name
}

terraform {
  backend "s3" {
    region = "us-east-1"
    bucket = "fileuploader-state" 
    key = "fileuploader/state"
  }
}

resource "aws_s3_bucket" "fileuploaderbucket" {
    bucket = var.bucket_name
    force_destroy = true
}

resource "aws_dynamodb_table" "fileuploadertable" {
    name = var.dynamo_table_name
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "file_id"

    attribute {
      name = "file_id"
      type = "S"
    }
}