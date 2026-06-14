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

# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambdarole" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "archive_file" "fileuploader_file" {
  type        = "zip"
  source_dir  = "${path.root}/../backend/src"
  output_path = "${path.root}/outputs/fileuploader.zip"
}

resource "aws_lambda_function" "fileuploader_function" {
  function_name = "fileuploader"
  role = aws_iam_role.lambdarole.arn

  filename = data.archive_file.fileuploader_file.output_path
  handler = "src.main.handler"
  runtime = "python3.12"

  # detect changes in zip file 
  source_code_hash = data.archive_file.fileuploader_file.output_base64sha256

  timeout = 30
  memory_size = 512
}