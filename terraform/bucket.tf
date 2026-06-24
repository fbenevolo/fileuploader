resource "aws_s3_bucket" "fileuploaderbucket" {
    bucket = var.bucket_name
    force_destroy = true
}