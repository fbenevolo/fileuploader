# api gateway resource definition
resource "aws_apigatewayv2_api" "fileuploader_api" {
  name          = "fileuploader-api"
  protocol_type = "HTTP"
}

# integration with lambda
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.fileuploader_function.invoke_arn
}

# ======================== routes ========================

resource "aws_apigatewayv2_route" "list_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "GET /list"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "upload_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "POST /upload"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "download_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "GET /downloads"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


resource "aws_apigatewayv2_route" "delete_route" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  route_key = "DELETE /delete"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# =========================================================

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.fileuploader_api.id
  name = "$default"
  auto_deploy = true
}
