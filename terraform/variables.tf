variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project identifier used for naming resources"
  type        = string
  default     = "lead-intelligence"
}

variable "google_places_api_key" {
  description = "Google Places API key"
  type        = string
  sensitive   = true  # Prevents key from appearing in logs
}

variable "search_configs" {
  description = "List of industry + location pairs to search"
  type = list(object({
    industry = string
    location = string
  }))
  default = [
    { industry = "plumbing",  location = "Port of Spain, Trinidad" },
    { industry = "dentist",   location = "Port of Spain, Trinidad" },
    { industry = "electrician", location = "Port of Spain, Trinidad" }
  ]
}