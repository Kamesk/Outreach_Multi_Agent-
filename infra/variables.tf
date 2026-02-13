variable "aws_region" {
  default = "eu-west-2"
}

variable "project_name" {
  default = "outreach-agent"
}

variable "vpc_id" {
  description = "xxxxxxx"
}

variable "public_subnets" {
  type = list(string)
}

variable "certificate_arn" {
  description = "xxxxxxxxx"
}
