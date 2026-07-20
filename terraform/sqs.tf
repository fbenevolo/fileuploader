resource "aws_sqs_queue" "metadata_queue" {
  name = "metadata-queue"
  visibility_timeout_seconds = 60
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}