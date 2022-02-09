######################################################################################################
# CLOUDWATCH CONFIGURATION
######################################################################################################

resource "aws_cloudwatch_metric_alarm" "domain_check" {
  alarm_name          = trimsuffix(local.name, "-")
  alarm_description   = "Alarm for ${var.health_check_domain_name} Health Check"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "HTTPS Health Check for ${var.health_check_domain_name}"
  namespace           = "PrivateHealthCheck"
  datapoints_to_alarm = "2"
  period              = "60"
  statistic           = "Minimum"
  threshold           = "1"
  treat_missing_data  = "breaching"
  actions_enabled     = true
  dimensions = {
    "Name" : "HTTPS Health Check",
    "Value" : "HTTPS Health Check"
  }
  alarm_actions             = [aws_sns_topic.alert.arn]
  ok_actions                = [aws_sns_topic.alert.arn]
  insufficient_data_actions = []
}