resource "aws_ssm_parameter" "google_api_key" {
  name        = "/${var.project_name}/google-places-api-key"
  description = "Google Places API key for lead collection"
  type        = "SecureString"   # Encrypted at rest using KMS
  value       = var.google_places_api_key

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}