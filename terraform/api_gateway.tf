# ======================== API ========================

resource "aws_apigatewayv2_api" "fileuploader_api" {
  name          = "fileuploader-api"
  protocol_type = "HTTP"
}


# ======================== integrations ========================

resource "aws_apigatewayv2_integration" "file_lambda_integration" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.file_function.invoke_arn
}


resource "aws_apigatewayv2_integration" "metadata_lambda_integration" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.metadata_api_function.invoke_arn
}


# ======================== file-service routes ========================

resource "aws_apigatewayv2_route" "upload_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "POST /upload"
  target = "integrations/${aws_apigatewayv2_integration.file_lambda_integration.id}"
}


resource "aws_apigatewayv2_route" "download_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "GET /download/{stored_name}"
  target = "integrations/${aws_apigatewayv2_integration.file_lambda_integration.id}"
}


resource "aws_apigatewayv2_route" "delete_file_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "DELETE /delete/{stored_name}"
  target = "integrations/${aws_apigatewayv2_integration.file_lambda_integration.id}"
}


# ======================== metadata-service routes ========================

resource "aws_apigatewayv2_route" "list_metadata_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "GET /metadata/list"
  target = "integrations/${aws_apigatewayv2_integration.metadata_lambda_integration.id}"
}

# ======================== stage ========================

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  name = "$default"
  auto_deploy = true
}