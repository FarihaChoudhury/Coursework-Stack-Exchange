# Say what cloud provider we're working with

provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}


# RDS TO STORE STACKEXCHANGE SCRAPED DATA 
resource "aws_db_instance" "stackexchange-db" {
    allocated_storage            = 10
    db_name                      = "c11farihastackexchangedb"
    identifier                   = "c11-fariha-stack-exchange-db"
    engine                       = "postgres"
    engine_version               = "16.1"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = "c11-public-subnet-group"
    vpc_security_group_ids       = [aws_security_group.c11-fariha-stack-exchange-RDS-sg-terrafrom.id]
    # sg-0ce13082d76a6ba2e ^
    username                     = var.DB_USERNAME
    password                     = var.DB_PASSWORD
}

resource "aws_security_group" "c11-fariha-stack-exchange-RDS-sg-terrafrom" {
    name = "c11-fariha-stack-exchange-RDS-sg-terrafrom"
    description = "Security group for connecting to RDS database"
    vpc_id = data.aws_vpc.c11-vpc.id

    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks      = ["0.0.0.0/0"]
    }
}

data "aws_vpc" "c11-vpc" {
    id = "vpc-04b15cce2398e57f7"
}


# ECS TASK - TO RUN PIPELINE: 
data "aws_ecs_cluster" "c11-cluster" {
    cluster_name = "c11-ecs-cluster"
}

data "aws_iam_role" "execution-role" {
    name = "ecsTaskExecutionRole"
}

resource "aws_ecs_task_definition" "c11-Fariha-stack-exchange-ECS-pipeline-terraform" {
  family = "c11-Fariha-stack-exchange-ECS-pipeline-terraform"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  execution_role_arn = data.aws_iam_role.execution-role.arn
  cpu = 1024
  memory = 2048
  container_definitions = jsonencode([
    {
      name = "c11-Fariha-stack-exchange-ECS-pipeline-terraform"
      image = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-fariha-stack-exchange-pipeline:latest"
      cpu = 10
      memory = 512
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment= [
                {
                    "name": "ACCESS_KEY",
                    "value": var.AWS_ACCESS_KEY
                },
                {
                    "name": "SECRET_ACCESS_KEY",
                    "value": var.AWS_SECRET_KEY
                },
                {
                    "name": "DB_NAME",
                    "value": var.DB_NAME
                },
                {
                    "name": "DB_USERNAME",
                    "value": var.DB_USERNAME
                },
                {
                    "name": "DB_PASSWORD",
                    "value": var.DB_PASSWORD
                },
                {
                    "name": "DB_IP",
                    "value": var.DB_IP
                },
                {
                    "name": "DB_PORT",
                    "value": var.DB_PORT
                }
            ]
            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    "awslogs-create-group" = "true"
                    "awslogs-group" = "/ecs/c11-Fariha-stack-exchange-ECS-pipeline-terraform"
                    "awslogs-region" = "eu-west-2"
                    "awslogs-stream-prefix" = "ecs"
                }
            }
    },
  ])
}



# EVENT BRIDGE - SCHEDULE ETL EVERY 9AM 
data "aws_subnet" "c11-subnet-1" {
  id = "subnet-0e6c6a8f959dae31a"
}
data "aws_subnet" "c11-subnet-2" {
  id = "subnet-08781450402b81aa2"
}
data "aws_subnet" "c11-subnet-3" {
  id = "subnet-07de213eeae1f6307"
}

data "aws_iam_policy_document" "c11-Fariha-event-bridge-policy-document-terraform" {
    statement {
            actions    = ["sts:AssumeRole"]
            effect     = "Allow"
            principals {
                type        = "Service"
                identifiers = ["scheduler.amazonaws.com"]
            }
    }
}

resource "aws_iam_role" "c11-Fariha-stack-exchange-etl-schedule-role-terraform"{
    name= "c11-Fariha-stack-exchange-etl-schedule-role-terraform"
    assume_role_policy = data.aws_iam_policy_document.c11-Fariha-event-bridge-policy-document-terraform.json

}
resource "aws_iam_role_policy" "c11-Fariha-stack-exchange-etl-schedule-role-policy-terraform" {
    # attach policies to role: call state machine, send email and invoke lambda
    name = "c11-Fariha-stack-exchange-etl-schedule-role-policy-terraform"
    role = aws_iam_role.c11-Fariha-stack-exchange-etl-schedule-role-terraform.id
    policy = jsonencode({
    Statement = [ 
        {
            Action = ["ecs:RunTask"],
            Effect = "Allow",
            Resource = "${aws_ecs_task_definition.c11-Fariha-stack-exchange-ECS-pipeline-terraform.arn}"
            Condition = {
                ArnLike = {"ecs:cluster" = data.aws_ecs_cluster.c11-cluster.arn}
            }
        },
        {
            Action =  ["iam:PassRole"]
            Effect   = "Allow"
            Resource = "*"
            Condition = {
                StringLike = {"iam:PassedToService" = "ecs-tasks.amazonaws.com"}
            }
        },

    ]
  })
}


resource "aws_scheduler_schedule" "c11-Fariha-stack-exchange-etl-schedule-terraform" {
    name       = "c11-Fariha-stack-exchange-etl-schedule-terraform"
    group_name = "default"
    
    flexible_time_window {
        mode = "OFF"
    }
    
    schedule_expression = "cron(0 9 * * ? *)"
    schedule_expression_timezone = "Europe/London"
    
    target {
        arn = data.aws_ecs_cluster.c11-cluster.arn
        role_arn = aws_iam_role.c11-Fariha-stack-exchange-etl-schedule-role-terraform.arn

        ecs_parameters {
            task_definition_arn = aws_ecs_task_definition.c11-Fariha-stack-exchange-ECS-pipeline-terraform.arn
            launch_type = "FARGATE"

            network_configuration {
                assign_public_ip = true
                subnets          = [data.aws_subnet.c11-subnet-1.id, data.aws_subnet.c11-subnet-2.id, data.aws_subnet.c11-subnet-3.id] 
            }
        }
    }
}



# ECS FOR DASHBOARD:
resource "aws_ecs_task_definition" "c11-Fariha-stack-exchange-ECS-dashboard-terraform" {
  family = "c11-Fariha-stack-exchange-ECS-dashboard-terraform"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  execution_role_arn = data.aws_iam_role.execution-role.arn
  cpu = 1024
  memory = 2048
  container_definitions = jsonencode([
    {
      name = "c11-Fariha-stack-exchange-ECS-dashboard-terraform"
      image = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-fariha-stack-exchange-dashboard:latest"
      cpu = 10
      memory = 512
      essential = true
      portMappings = [
        {
            containerPort = 80
            hostPort = 80
        },
        {
            containerPort = 8501
            hostPort = 8501       
        }
      ]
      environment= [
                {
                    "name": "ACCESS_KEY",
                    "value": var.AWS_ACCESS_KEY
                },
                {
                    "name": "SECRET_ACCESS_KEY",
                    "value": var.AWS_SECRET_KEY
                },
                {
                    "name": "DB_NAME",
                    "value": var.DB_NAME
                },
                {
                    "name": "DB_USERNAME",
                    "value": var.DB_USERNAME
                },
                {
                    "name": "DB_PASSWORD",
                    "value": var.DB_PASSWORD
                },
                {
                    "name": "DB_IP",
                    "value": var.DB_IP
                },
                {
                    "name": "DB_PORT",
                    "value": var.DB_PORT
                }
            ]
            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    "awslogs-create-group" = "true"
                    "awslogs-group" = "/ecs/c11-Fariha-stack-exchange-ECS-dashboard-terraform"
                    "awslogs-region" = "eu-west-2"
                    "awslogs-stream-prefix" = "ecs"
                }
            }
    },
  ])
}


# SERVICE TO START DASHBOARD:

resource "aws_security_group" "c11-fariha-stack-exchange-dashboard-sg-terraform" {
    name = "c11-fariha-stack-exchange-dashboard-sg-terraform"
    description = "Security group for connecting to dashboard"
    vpc_id = data.aws_vpc.c11-vpc.id

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port   = 8501
        to_port     = 8501
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }


}

resource "aws_ecs_service" "c11-Fariha-stack-exchange-ECS-dashboard-service-terraform" {
    name = "c11-Fariha-dashboard-service-terraform"
    cluster = data.aws_ecs_cluster.c11-cluster.id
    task_definition = aws_ecs_task_definition.c11-Fariha-stack-exchange-ECS-dashboard-terraform.arn
    desired_count = 1
    launch_type = "FARGATE" 
    
    network_configuration {
        subnets = [data.aws_subnet.c11-subnet-1.id, data.aws_subnet.c11-subnet-2.id, data.aws_subnet.c11-subnet-3.id] 
        security_groups = [aws_security_group.c11-fariha-stack-exchange-dashboard-sg-terraform.id] 
        # ^ ["sg-03f4c8759b7419953"] the security group ^
        assign_public_ip = true
    }
}