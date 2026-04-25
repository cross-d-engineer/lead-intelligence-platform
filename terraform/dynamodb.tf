resource "aws_dynamodb_table" "leads" {
  name         = "${var.project_name}-leads"
  billing_mode = "PAY_PER_REQUEST"  # Free tier + no capacity planning needed
  hash_key     = "place_id"         # Matches our deduplication key

  attribute {
    name = "place_id"
    type = "S"
  }

  attribute {
    name = "industry"
    type = "S"
  }

  attribute {
    name = "city"
    type = "S"
  }

  # Global Secondary Indexes for query flexibility
  global_secondary_index {
    name            = "industry-index"
    hash_key        = "industry"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "city-index"
    hash_key        = "city"
    projection_type = "ALL"
  }

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}