resource "aws_s3_bucket" "fileuploaderbucket" {
    bucket = var.bucket_name
    force_destroy = true
}

resource "aws_s3_bucket_notification" "file_created" {
  bucket = aws_s3_bucket.fileuploaderbucket.id
  
  queue {
    queue_arn = aws_sqs_queue.metadata_queue.arn
    events = [
      "s3:ObjectCreated:*"
    ]
  }

}