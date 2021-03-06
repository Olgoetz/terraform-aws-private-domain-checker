######################################################################################################
# EVENTS CONFIGURATION
######################################################################################################

# Cron expression
resource "aws_cloudwatch_event_rule" "health_check" {
  name                = "${local.name}CW-EventRule-${random_id.this.hex}"
  description         = "Perform a health check on ${var.health_check_domain_name}."
  schedule_expression = "cron(1/${var.cw_cron_interval} * * * ? *)"
}

# Define the lambda function as target
resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.health_check.name
  target_id = "TriggerLambda${random_id.this.hex}"
  arn       = aws_lambda_function.this.arn
}

# Permissions
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch${random_id.this.hex}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.health_check.arn
}
