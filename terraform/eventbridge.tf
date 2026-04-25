# Run the collector every Monday at 8am UTC
resource "aws_cloudwatch_event_rule" "weekly_collection" {
  name                = "${var.project_name}-weekly-trigger"
  description         = "Triggers lead collection weekly"
  schedule_expression = "cron(0 8 ? * MON *)"
}

resource "aws_cloudwatch_event_target" "trigger_lambda" {
  rule      = aws_cloudwatch_event_rule.weekly_collection.name
  target_id = "CollectorLambda"
  arn       = aws_lambda_function.collector.arn
}

# Permission for EventBridge to invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.collector.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly_collection.arn
}