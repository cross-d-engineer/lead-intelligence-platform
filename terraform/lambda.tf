# Package pipeline code
data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/../pipeline"
  output_path = "${path.module}/lambda_package.zip"
}

# Package dependencies as a Lambda Layer
data "archive_file" "lambda_layer" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda_layer"
  output_path = "${path.module}/lambda_layer.zip"
}

resource "aws_lambda_layer_version" "dependencies" {
  filename            = data.archive_file.lambda_layer.output_path
  layer_name          = "${var.project_name}-dependencies"
  compatible_runtimes = ["python3.11"]
  source_code_hash    = data.archive_file.lambda_layer.output_base64sha256
}

resource "aws_lambda_function" "collector" {
  function_name    = "${var.project_name}-collector"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_handler.handler"
  runtime          = "python3.11"
  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  timeout          = 300
  memory_size      = 256

  # Attach the dependencies layer
  layers = [aws_lambda_layer_version.dependencies.arn]

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.leads.name
      S3_BUCKET      = aws_s3_bucket.raw_responses.bucket
      SSM_PARAM_NAME = aws_ssm_parameter.google_api_key.name
      SEARCH_CONFIGS = jsonencode(var.search_configs)
    }
  }

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}