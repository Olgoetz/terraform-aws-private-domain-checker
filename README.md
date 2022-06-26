# AWS PRIVATE DOMAIN CHECKER Terraform Module

A Terraform module to provision a domain health checker for private applications
hosted in a private subnet.

## Features

- [x] Cron Job customizable
- [x] CloudWatch Alarm populates to SNS topic
- [x] Subscribers can be provided by email addresses
- [x] 503 and 502 listener rules for ELB with customizable html content

## Examples

Look into `./examples`

## Usage

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.1.4 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.1.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 4.1.0 |
| <a name="provider_random"></a> [random](#provider\_random) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_lambda-layer"></a> [lambda-layer](#module\_lambda-layer) | ./lambda-layer | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.health_check](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_metric_alarm.domain_check](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_iam_role.role_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy.policy_role_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy_attachment.policy_attachment_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.allow_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_sns_topic.alert](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.email](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription) | resource |
| [random_id.this](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/id) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_caller_identity.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.assume_role_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.policy_role_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_kms_alias.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/kms_alias) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | Provisioning region | `string` | `"eu-central-1"` | no |
| <a name="input_create_lambda_layer"></a> [create\_lambda\_layer](#input\_create\_lambda\_layer) | Create lambda layer specific for this tool | `bool` | `true` | no |
| <a name="input_cw_cron_interval"></a> [cw\_cron\_interval](#input\_cw\_cron\_interval) | Cron interval in minutes to schedule the health check | `number` | `1` | no |
| <a name="input_default_tags"></a> [default\_tags](#input\_default\_tags) | Tags to apply to all resources | `map(any)` | `{}` | no |
| <a name="input_health_check_domain_name"></a> [health\_check\_domain\_name](#input\_health\_check\_domain\_name) | Domain name for the health check | `string` | n/a | yes |
| <a name="input_health_check_path"></a> [health\_check\_path](#input\_health\_check\_path) | Health check path (without '/') | `string` | n/a | yes |
| <a name="input_health_check_port"></a> [health\_check\_port](#input\_health\_check\_port) | Health check port | `string` | `"443"` | no |
| <a name="input_html_path_502"></a> [html\_path\_502](#input\_html\_path\_502) | Path to a html file for a 502 fixed response | `string` | n/a | yes |
| <a name="input_html_path_503"></a> [html\_path\_503](#input\_html\_path\_503) | Path to a html file for a 503 fixed response | `string` | n/a | yes |
| <a name="input_kms_key_alias"></a> [kms\_key\_alias](#input\_kms\_key\_alias) | KMS key alias (e.g. alias/mykms) for SNS encryption at rest. Permissions for cloudwatch must be added to this as well https://aws.amazon.com/de/premiumsupport/knowledge-center/cloudwatch-receive-sns-for-alarm-trigger/. | `string` | `""` | no |
| <a name="input_lambda_layer_arn"></a> [lambda\_layer\_arn](#input\_lambda\_layer\_arn) | ARN of a lambda layer (MUST have the python package requests installed) | `string` | `""` | no |
| <a name="input_listener_arn"></a> [listener\_arn](#input\_listener\_arn) | ARN of the ALB listener | `string` | n/a | yes |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | Prefix for all created resources (e.g. ApplicationX-) | `string` | n/a | yes |
| <a name="input_sns_email_addresses"></a> [sns\_email\_addresses](#input\_sns\_email\_addresses) | List of email addresses to send reports to | `list(string)` | `[]` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | Subnet ids | `list(string)` | n/a | yes |
| <a name="input_verify_ssl"></a> [verify\_ssl](#input\_verify\_ssl) | Verify SSL (1 = True, 0 = False) | `string` | `"1"` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC id | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cw_alarm_arn"></a> [cw\_alarm\_arn](#output\_cw\_alarm\_arn) | ARN of the CloudWatch alarm |
| <a name="output_lambda_function_arn"></a> [lambda\_function\_arn](#output\_lambda\_function\_arn) | ARN of the lambda function that conducts the health check |
| <a name="output_lambda_role_arn"></a> [lambda\_role\_arn](#output\_lambda\_role\_arn) | Role ARN of the lambda function that conducts the health check |
| <a name="output_sns_topic_arn"></a> [sns\_topic\_arn](#output\_sns\_topic\_arn) | ARN of the SNS topic CloudWatch sends alarms to |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
