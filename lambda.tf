######################################################################################################
# LAMBDA CONFIGURATION
######################################################################################################

data "archive_file" "this" {
  output_path = "${path.module}/payload.zip"
  type        = "zip"
  source_dir  = "${path.module}/sources"
}

# Function
resource "aws_lambda_function" "this" {
  function_name    = "${local.name}Lambda-${random_id.this.hex}"
  filename         = data.archive_file.this.output_path
  source_code_hash = data.archive_file.this.output_base64sha256
  handler          = "main.handler"
  role             = aws_iam_role.role_lambda.arn
  runtime          = "python3.9"
  timeout          = "120"

  vpc_config {
    security_group_ids = [aws_security_group.this.id]
    subnet_ids         = var.subnet_ids
  }

  environment {
    variables = {
      verify_ssl               = var.verify_ssl
      health_check_domain_name = var.health_check_domain_name
      health_check_path        = var.health_check_path
      port                     = var.health_check_port
      listener_arn             = var.listener_arn
      html_path_502            = var.html_path_502
      html_path_503            = var.html_path_503
    }
  }
}

## IAM
# ------------------------------------------------------------------------------------
resource "aws_iam_role" "role_lambda" {
  assume_role_policy = data.aws_iam_policy_document.assume_role_lambda.json
  name               = "${local.name}LambdaRole-${random_id.this.hex}"
}

# Assume role policy
data "aws_iam_policy_document" "assume_role_lambda" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
  }
}


# Lambda role policy
data "aws_iam_policy_document" "policy_role_lambda" {
  statement {
    sid       = 1
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = ["arn:aws:lambda:${var.aws_region}:${data.aws_caller_identity.this.account_id}:function:${local.name}Lambda"]
  }

  statement {
    sid = 2
    actions = [
      "elasticloadbalancing:CreateRule",
    "elasticloadbalancing:DeleteRule"]
    resources = [var.listener_arn]
  }
  statement {
    sid       = 3
    actions   = ["cloudwatch:PutMetricData"]
    resources = ["*"]
  }
}

# Policy resource
resource "aws_iam_role_policy" "policy_role_lambda" {
  name   = "${local.name}-LambdaPolicy-${random_id.this.hex}"
  policy = data.aws_iam_policy_document.policy_role_lambda.json
  role   = aws_iam_role.role_lambda.id
}

# VPC basic execution role
resource "aws_iam_role_policy_attachment" "policy_attachment_lambda" {
  role       = aws_iam_role.role_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}


## Logging
# ------------------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${local.name}Lambda-${random_id.this.hex}"
  retention_in_days = 3
}

## Network
# ------------------------------------------------------------------------------------
# Security Group
resource "aws_security_group" "this" {
  name   = "${local.name}SG-${random_id.this.hex}"
  vpc_id = var.vpc_id

  egress {
    from_port   = 0
    protocol    = -1
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(tomap({ "Name" = "${local.name}SG-${random_id.this.hex}" }), var.default_tags)
}