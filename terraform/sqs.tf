resource "aws_sqs_queue" "metadata_queue" {
  name = "metadata-queue"
  visibility_timeout_seconds = 60
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}

resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.metadata_queue.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action = "sqs:SendMessage"
        Resource = aws_sqs_queue.metadata_events.arn
      }
    ]
  })
}