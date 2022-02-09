# General
# ------------------------------------------------------------------------------------

variable "default_tags" {
  type        = map(any)
  description = "Tags to apply to all resources"
  default     = {}
}

variable "aws_region" {
  type        = string
  description = "Provisioning region"
  default     = "eu-central-1"
}

variable "resource_prefix" {
  type        = string
  description = "Prefix for all created resources (e.g. ApplicationX-)"
}

# Network
# ------------------------------------------------------------------------------------

variable "vpc_id" {
  type        = string
  description = "VPC id"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet ids"
}

# Events
# ------------------------------------------------------------------------------------

variable "cw_cron_expression" {
  type        = string
  description = "Cron job to schedule the health check"
  default     = "cron(1/5 * * * ? *)"
}


# SNS
# ------------------------------------------------------------------------------------

variable "kms_key_alias" {
  type        = string
  description = "KMS key alias (e.g. alias/mykms) for SNS encryption at rest. Permissions for cloudwatch must be added to this as well https://aws.amazon.com/de/premiumsupport/knowledge-center/cloudwatch-receive-sns-for-alarm-trigger/"
  default     = ""
}

variable "sns_email_addresses" {
  type        = list(string)
  description = "List of email addresses to send reports to"
  default     = []
}

# Lambda env variables

variable "verify_ssl" {
  type        = string
  description = "Verify SSL (1 = True, 0 = False)"
  default     = "1"
}


variable "health_check_path" {
  type        = string
  description = "Health check path (without '/')"
}

variable "health_check_port" {
  type        = string
  description = "Health check port"
  default     = "443"
}

variable "health_check_domain_name" {
  type        = string
  description = "Domain name for the health check"

}