variable "lambda_key" {
  type = string 
}

# data "archive_file" "fileuploader_file" {
#   type        = "zip"
#   source_dir  = "${path.root}/../backend/src"
#   output_path = "${path.root}/outputs/fileuploader.zip"
# }

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

# ==========================================================================

# ================================ function ================================ 

resource "aws_lambda_function" "fileuploader_function" {
  function_name = "fileuploader"
  role = aws_iam_role.lambdarole.arn

  s3_bucket = "fileuploader-zip"
  s3_key = var.lambda_key

  # filename = data.archive_file.fileuploader_file.output_path
  handler = "main.handler"
  runtime = "python3.12"

  # detect changes in zip file 
  # source_code_hash = data.archive_file.fileuploader_file.output_base64sha256

  timeout = 30
  memory_size = 512
}

# ==========================================================================

# ========================= api gateway permission =========================
resource "aws_lambda_permission" "apigateway_permission" {
  statement_id = "AllowAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fileuploader_function.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.fileuploader_api.execution_arn}/*/*"
}
# ==========================================================================
