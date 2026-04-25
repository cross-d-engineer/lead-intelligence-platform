# Trust policy — allows Lambda service to assume this role
data "aws_iam_policy_document" "lambda_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "${var.project_name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

# Permissions the Lambda function needs
data "aws_iam_policy_document" "lambda_permissions" {
  # CloudWatch Logs — required for any Lambda logging
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }

  # DynamoDB — read/write leads table only
  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:Query",
      "dynamodb:Scan"
    ]
    resources = [
      aws_dynamodb_table.leads.arn,
      "${aws_dynamodb_table.leads.arn}/index/*"
    ]
  }

  # S3 — write raw responses only
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.raw_responses.arn}/*"]
  }

  # SSM — read API key only
  statement {
    actions   = ["ssm:GetParameter"]
    resources = [aws_ssm_parameter.google_api_key.arn]
  }
}

resource "aws_iam_role_policy" "lambda_exec_policy" {
  name   = "${var.project_name}-lambda-policy"
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.lambda_permissions.json
}