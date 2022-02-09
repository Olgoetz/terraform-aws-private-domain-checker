output "lambda_function_arn" {
  value       = aws_lambda_function.this.arn
  description = "ARN of the lambda function that conducts the health check"
}

output "lambda_role_arn" {
  value       = aws_iam_role.role_lambda.arn
  description = "Role ARN of the lambda function that conducts the health check"
}

output "cw_alarm_arn" {
  value       = aws_cloudwatch_metric_alarm.domain_check.arn
  description = "ARN of the CloudWatch alarm"
}

output "sns_topic_arn" {
  value       = aws_sns_topic.alert.arn
  description = "ARN of the SNS topic CloudWatch sends alarms to"
}