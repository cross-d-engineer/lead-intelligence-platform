resource "aws_s3_bucket" "raw_responses" {
  # Bucket names must be globally unique — project name + account suffix handles this
  bucket = "${var.project_name}-raw-responses-${data.aws_caller_identity.current.account_id}"

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

# Block all public access — this bucket is internal only
resource "aws_s3_bucket_public_access_block" "raw_responses" {
  bucket = aws_s3_bucket.raw_responses.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Get current AWS account ID for unique bucket naming
data "aws_caller_identity" "current" {}