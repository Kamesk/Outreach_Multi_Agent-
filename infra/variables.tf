variable "aws_region" { type = string; default = "eu-west-2" }
variable "project_name" { type = string; default = "outreach-agent" }
variable "image_tag" { type = string; description = "Immutable image tag, normally the Git commit SHA." }
variable "vpc_id" { type = string }
variable "public_subnets" { type = list(string) }
variable "private_subnets" { type = list(string) }
variable "certificate_arn" { type = string }
variable "bucket_arn" { type = string }
variable "dynamodb_table_arns" { type = list(string) }
variable "workflow_table_name" { type = string; default = "OutreachWorkflows" }
variable "sns_topic_arns" { type = list(string); default = [] }
variable "secret_arns" { type = map(string); sensitive = true }
variable "kms_key_arns" { type = list(string); default = ["*"] }
variable "allowed_ingress_cidrs" { type = list(string); default = ["0.0.0.0/0"] }
variable "desired_count" { type = number; default = 2 }
variable "log_retention_days" { type = number; default = 90 }
variable "deletion_protection" { type = bool; default = true }
