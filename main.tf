locals {
  name = "${var.resource_prefix}DomainHealthCheck-"
}

data "aws_caller_identity" "this" {}

data "aws_kms_alias" "this" {
  count = var.kms_key_alias != "" ? 1 : 0
  name  = var.kms_key_alias
}


module "lambda-layer" {
  count      = var.create_lambda_layer ? 1 : 0
  source     = "./lambda-layer"
  layer_name = "${local.name}LambdaLayer-${random_id.this.hex}"
}