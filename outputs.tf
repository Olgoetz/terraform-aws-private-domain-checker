output "lambda_function_arn" {
  value = aws_lambda_function.this.arn
}

output "cw_alarm_arn" {
  value = aws_cloudwatch_metric_alarm.domain_check.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.role_lambda.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.alert.arn
}