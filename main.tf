locals {
  name = "${var.resource_prefix}DomainHealthCheck-"
}

data "aws_caller_identity" "this" {}

data "aws_kms_alias" "this" {
  count = var.kms_key_alias != "" ? 1 : 0
  name  = var.kms_key_alias
}
