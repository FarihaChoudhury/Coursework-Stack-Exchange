# Say what cloud provider we're working with

provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

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
    vpc_security_group_ids       = [aws_security_group.db-security-group.id]
    username                     = var.DB_USERNAME
    password                     = var.DB_PASSWORD
}

resource "aws_security_group" "db-security-group" {
    name = "c11-fariha-stack-exchange-sg"
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