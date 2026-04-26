terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }


  backend "s3" {
  bucket          = "lead-intelligence-tfstate-552433024151"
  key             = "prod/terraform.tfstate"
  region          = "us-east-1"
  dynamodb_table  = "lead-intelligence-tfstate-lock"
  encrypt         = true
  }
}

provider "aws" {
  region = var.aws_region
}