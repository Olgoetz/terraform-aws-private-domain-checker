
variable "aws_region" {
  type        = string
  description = "Provisioning region"
  default     = "eu-central-1"
}

variable "resource_prefix" {
  type        = string
  description = "Prefix for all created resources (e.g. ApplicationX-)"
  default     = "MyTest-"
}


provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {}
  }
}

module "create_domain_health_check" {
  source                   = "../"
  health_check_domain_name = "users.tfe-nonprod.aws-cloud.axa-de.intraxa"
  health_check_path        = "_health_check"
  resource_prefix          = var.resource_prefix
  subnet_ids               = ["subnet-092eafe62ad31610f"]
  vpc_id                   = "vpc-0b15ec82229c433c0"
  sns_email_addresses      = ["oliver.goetz@axa.com"]
  verify_ssl               = "0"
  cw_cron_interval         = 30
}

output "lambda_function_arn" {
  value = module.create_domain_health_check.lambda_function_arn
}

output "cw_alarm_arn" {
  value = module.create_domain_health_check.cw_alarm_arn
}

output "lambda_role_arn" {
  value = module.create_domain_health_check.lambda_role_arn
}

output "sns_topic_arn" {
  value = module.create_domain_health_check.sns_topic_arn
}