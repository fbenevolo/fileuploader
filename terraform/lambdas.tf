variable "lambda_key" {
  type = string 
}

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


# ================================ policies ================================ 

resource "aws_iam_role_policy_attachment" "s3_permission" {
  role = aws_iam_role.lambdarole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "dynamo_permission" {
  role = aws_iam_role.lambdarole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess_v2"
}

resource "aws_iam_role_policy_attachment" "logs_permission" {
  role = aws_iam_role.lambdarole.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_role_policy_attachment" "sqs_permission" {
  role = aws_iam_role.lambdarole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

# ==========================================================================

# ================================ functions ================================ 

resource "aws_lambda_function" "file_function" {
  function_name = "file-service"
  role = aws_iam_role.lambdarole.arn

  s3_bucket = "file-service-zip"
  s3_key = var.lambda_key

  # filename = data.archive_file.fileuploader_file.output_path
  handler = "main.handler"
  runtime = "python3.12"

  # detect changes in zip file 
  # source_code_hash = data.archive_file.fileuploader_file.output_base64sha256

  timeout = 30
  memory_size = 512

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.fileuploaderbucket.bucket
    }
  }
}

# resource "aws_lambda_function" "metadata_function" {
#   function_name = "metadata-service"
#   role = aws_iam_role.lambdarole.arn

#   s3_bucket = "metadata-service-zip"
#   s3_key = var.lambda_key

#   # filename = data.archive_file.fileuploader_file.output_path
#   handler = "main.handler"
#   runtime = "python3.12"

#   # detect changes in zip file 
#   # source_code_hash = data.archive_file.fileuploader_file.output_base64sha256

#   timeout = 30
#   memory_size = 512

#   environment {
#     variables = {
#       BUCKET_NAME = aws_s3_bucket.fileuploaderbucket.bucket
#       DYNAMO_TABLE = aws_dynamodb_table.fileuploadertable.name
#     }
#   }
# }

resource "aws_lambda_function" "metadata_api_function" {
  function_name = "metadata-api-service"
  role = aws_iam_role.lambdarole.arn

  s3_bucket = "metadata-service-zip"
  s3_key = var.lambda_key

  handler = "main.handler"

  runtime = "python3.12"

  timeout = 30
  memory_size = 512

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.fileuploaderbucket.bucket
      DYNAMO_TABLE = aws_dynamodb_table.fileuploadertable.name
    }
  }
}

resource "aws_lambda_function" "metadata_worker_function" {
  function_name = "metadata-worker-service"
  role = aws_iam_role.lambdarole.arn
  
  s3_bucket = "metadata-service-zip"
  s3_key = var.lambda_key
  
  handler = "sqs_handler.handler"
  runtime = "python3.12"

  timeout = 30
  memory_size = 512

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.fileuploaderbucket.bucket
      DYNAMO_TABLE = aws_dynamodb_table.fileuploadertable.name
    }
  }
}

# ==========================================================================

# ========================= api gateway permission =========================

resource "aws_lambda_permission" "file_apigateway_permission" {
  statement_id = "AllowAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_function.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.fileuploader_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "metadata_apigateway_permission" {
  statement_id = "AllowAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.metadata_function.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.fileuploader_api.execution_arn}/*/*"
}

# ==========================================================================

# ========================= metadata trigger ===============================

resource "aws_lambda_event_source_mapping" "metadata_sqs_trigger" {
  event_source_arn = aws_sqs_queue.metadata_queue.arn
  function_name = aws_lambda_function.metadata_function.function_name
  batch_size = 10
  enabled = true

}
