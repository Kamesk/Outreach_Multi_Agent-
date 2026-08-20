terraform {
  required_version = ">= 1.6"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}

provider "aws" { region = var.aws_region }

resource "aws_dynamodb_table" "workflows" {
  name = var.workflow_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "id"
  attribute { name = "id"; type = "S" }
  point_in_time_recovery { enabled = true }
  server_side_encryption { enabled = true }
}

resource "aws_ecr_repository" "agent_repo" {
  name = var.project_name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration { scan_on_push = true }
}
resource "aws_cloudwatch_log_group" "agent_logs" { name = "/ecs/${var.project_name}"; retention_in_days = var.log_retention_days }

data "aws_iam_policy_document" "assume_ecs" { statement { actions = ["sts:AssumeRole"]; principals { type = "Service"; identifiers = ["ecs-tasks.amazonaws.com"] } } }
resource "aws_iam_role" "execution" { name = "${var.project_name}-execution"; assume_role_policy = data.aws_iam_policy_document.assume_ecs.json }
resource "aws_iam_role_policy_attachment" "execution" { role = aws_iam_role.execution.name; policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy" }
data "aws_iam_policy_document" "execution_secrets" { statement { actions = ["secretsmanager:GetSecretValue"]; resources = values(var.secret_arns) } statement { actions = ["kms:Decrypt"]; resources = var.kms_key_arns } }
resource "aws_iam_role_policy" "execution_secrets" { name = "${var.project_name}-secrets"; role = aws_iam_role.execution.id; policy = data.aws_iam_policy_document.execution_secrets.json }
resource "aws_iam_role" "task" { name = "${var.project_name}-task"; assume_role_policy = data.aws_iam_policy_document.assume_ecs.json }
data "aws_iam_policy_document" "task" {
  statement { actions = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:Query"]; resources = concat(var.dynamodb_table_arns, [aws_dynamodb_table.workflows.arn]) }
  statement { actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"]; resources = [var.bucket_arn, "${var.bucket_arn}/*"] }
  statement { actions = ["sns:Publish"]; resources = var.sns_topic_arns }
}
resource "aws_iam_role_policy" "task" { name = "${var.project_name}-least-privilege"; role = aws_iam_role.task.id; policy = data.aws_iam_policy_document.task.json }
resource "aws_ecs_cluster" "agent" { name = "${var.project_name}-cluster" }

resource "aws_security_group" "alb" {
  name = "${var.project_name}-alb"; vpc_id = var.vpc_id
  ingress { from_port = 443; to_port = 443; protocol = "tcp"; cidr_blocks = var.allowed_ingress_cidrs }
  egress { from_port = 8000; to_port = 8000; protocol = "tcp"; security_groups = [aws_security_group.task.id] }
}
resource "aws_security_group" "task" {
  name = "${var.project_name}-task"; vpc_id = var.vpc_id
  ingress { from_port = 8000; to_port = 8000; protocol = "tcp"; security_groups = [aws_security_group.alb.id] }
  egress { from_port = 443; to_port = 443; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
}
resource "aws_lb" "agent" { name = "${var.project_name}-alb"; load_balancer_type = "application"; subnets = var.public_subnets; security_groups = [aws_security_group.alb.id]; drop_invalid_header_fields = true; enable_deletion_protection = var.deletion_protection }
resource "aws_lb_target_group" "agent" { name = "${var.project_name}-tg"; port = 8000; protocol = "HTTP"; vpc_id = var.vpc_id; target_type = "ip"; health_check { path = "/health"; matcher = "200"; interval = 30; timeout = 5; healthy_threshold = 2; unhealthy_threshold = 3 } }
resource "aws_lb_listener" "https" { load_balancer_arn = aws_lb.agent.arn; port = 443; protocol = "HTTPS"; ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"; certificate_arn = var.certificate_arn; default_action { type = "forward"; target_group_arn = aws_lb_target_group.agent.arn } }
resource "aws_ecs_task_definition" "agent" {
  family = var.project_name; requires_compatibilities = ["FARGATE"]; cpu = "512"; memory = "1024"; network_mode = "awsvpc"
  execution_role_arn = aws_iam_role.execution.arn; task_role_arn = aws_iam_role.task.arn
  container_definitions = jsonencode([{ name = var.project_name; image = "${aws_ecr_repository.agent_repo.repository_url}:${var.image_tag}"; essential = true; portMappings = [{ containerPort = 8000, protocol = "tcp" }]; readonlyRootFilesystem = true; linuxParameters = { initProcessEnabled = true }; logConfiguration = { logDriver = "awslogs", options = { awslogs-group = aws_cloudwatch_log_group.agent_logs.name, awslogs-region = var.aws_region, awslogs-stream-prefix = "ecs" } }; secrets = [for name, arn in var.secret_arns : { name = name, valueFrom = arn }]; environment = [{ name = "AWS_REGION", value = var.aws_region }, { name = "WORKFLOW_TABLE_NAME", value = aws_dynamodb_table.workflows.name }, { name = "ALLOW_LIVE_PUBLISH", value = "false" }] }])
}
resource "aws_ecs_service" "agent" {
  name = var.project_name; cluster = aws_ecs_cluster.agent.id; task_definition = aws_ecs_task_definition.agent.arn; desired_count = var.desired_count; launch_type = "FARGATE"; deployment_minimum_healthy_percent = 100; deployment_maximum_percent = 200; health_check_grace_period_seconds = 60
  network_configuration { subnets = var.private_subnets; security_groups = [aws_security_group.task.id]; assign_public_ip = false }
  load_balancer { target_group_arn = aws_lb_target_group.agent.arn; container_name = var.project_name; container_port = 8000 }
  depends_on = [aws_lb_listener.https]
}
resource "aws_cloudwatch_metric_alarm" "unhealthy" { alarm_name = "${var.project_name}-unhealthy-targets"; namespace = "AWS/ApplicationELB"; metric_name = "UnHealthyHostCount"; statistic = "Maximum"; period = 60; evaluation_periods = 2; threshold = 0; comparison_operator = "GreaterThanThreshold"; dimensions = { TargetGroup = aws_lb_target_group.agent.arn_suffix, LoadBalancer = aws_lb.agent.arn_suffix } }
