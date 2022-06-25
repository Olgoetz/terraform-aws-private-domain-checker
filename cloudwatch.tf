######################################################################################################
# CLOUDWATCH CONFIGURATION
######################################################################################################


resource "aws_cloudwatch_metric_alarm" "domain_check" {
  alarm_name          = "${local.name}${random_id.this.hex}"
  alarm_description   = "Alarm for ${var.health_check_domain_name} Health Check"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "HTTPS Health Check for ${var.health_check_domain_name}"
  namespace           = "PrivateHealthCheck"
  datapoints_to_alarm = "1"
  period              = var.cw_cron_interval * 60
  statistic           = "Minimum"
  threshold           = "1"
  treat_missing_data  = "breaching"
  actions_enabled     = true
  dimensions = {
    HTTPS-Health-Check = "HTTPS Health Check"
  }
  alarm_actions             = [aws_sns_topic.alert.arn]
  ok_actions                = [aws_sns_topic.alert.arn]
  insufficient_data_actions = []
}