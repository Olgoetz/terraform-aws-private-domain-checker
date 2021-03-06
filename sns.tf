resource "aws_sns_topic" "alert" {
  name              = "${local.name}SNS-AlertTopic-${random_id.this.hex}"
  kms_master_key_id = var.kms_key_alias != "" ? data.aws_kms_alias.this[0].name : null
}

resource "aws_sns_topic_subscription" "email" {
  for_each  = toset(var.sns_email_addresses)
  topic_arn = aws_sns_topic.alert.arn
  protocol  = "email"
  endpoint  = each.value
}