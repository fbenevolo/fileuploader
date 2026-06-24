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