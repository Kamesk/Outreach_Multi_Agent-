terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "eu-west-2"
}

variable "project_name" {
  default = "outreach-agent"
}

variable "vpc_id" {}
variable "public_subnets" {
  type = list(string)
}

variable "certificate_arn" {}

resource "aws_ecr_repository" "agent_repo" {
  name = var.project_name
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_cloudwatch_log_group" "agent_logs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 14
}

resource "aws_ecs_cluster" "agent_cluster" {
  name = "${var.project_name}-cluster"
}

resource "aws_ecs_task_definition" "agent_task" {
  family                   = var.project_name
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = var.project_name
      image     = "${aws_ecr_repository.agent_repo.repository_url}:latest"
      essential = true

      portMappings = [{
        containerPort = 8000
        protocol      = "tcp"
      }]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.agent_logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }

      environment = [
        { name = "OPENAI_API_KEY", value = "replace-in-secrets" },
        { name = "CLIENT_ID", value = "replace" },
        { name = "CLIENT_SECRET", value = "replace" },
        { name = "TENANT_ID", value = "replace" }
      ]
    }
  ])
}

resource "aws_security_group" "agent_sg" {
  name   = "${var.project_name}-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "agent_alb" {
  name               = "${var.project_name}-alb"
  load_balancer_type = "application"
  subnets            = var.public_subnets
  security_groups    = [aws_security_group.agent_sg.id]
}

resource "aws_lb_target_group" "agent_tg" {
  name        = "${var.project_name}-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.agent_alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.agent_tg.arn
  }
}

resource "aws_ecs_service" "agent_service" {
  name            = var.project_name
  cluster         = aws_ecs_cluster.agent_cluster.id
  task_definition = aws_ecs_task_definition.agent_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.public_subnets
    security_groups  = [aws_security_group.agent_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.agent_tg.arn
    container_name   = var.project_name
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.https_listener]
}
