provider "aws" {
  region = var.aws-region
}

resource "aws_vpc" "saintmtool-vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "Saintmtool-VPC"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_subnet" "public-subnet-1" {
  availability_zone = "eu-west-1a"
  cidr_block        = var.public_subnet_1_cidr
  vpc_id            = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Public-Subnet-1"
  }
}

resource "aws_subnet" "public-subnet-2" {
  availability_zone = "eu-west-1b"
  cidr_block        = var.public_subnet_2_cidr
  vpc_id            = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Public-Subnet-2"
  }
}

resource "aws_subnet" "private-subnet-1" {
  availability_zone = "eu-west-1a"
  cidr_block        = var.private_subnet_1_cidr
  vpc_id            = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Private-Subnet-1"
  }
}

resource "aws_subnet" "private-subnet-2" {
  availability_zone = "eu-west-1b"
  cidr_block        = var.private_subnet_2_cidr
  vpc_id            = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Private-Subnet-2"
  }
}

resource "aws_route_table" "public-route-table" {
  vpc_id = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Public-Route-Table"
  }
}

resource "aws_route_table" "private-route-table" {

  vpc_id = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Private-Route-Table"
  }
}

resource "aws_route_table_association" "public-subnet-1-association" {
  route_table_id = aws_route_table.public-route-table.id
  subnet_id      = aws_subnet.public-subnet-1.id
}

resource "aws_route_table_association" "public-subnet-2-association" {
  route_table_id = aws_route_table.public-route-table.id
  subnet_id      = aws_subnet.public-subnet-2.id
}

resource "aws_route_table_association" "private-subnet-1-association" {
  route_table_id = aws_route_table.private-route-table.id
  subnet_id      = aws_subnet.private-subnet-1.id
}

resource "aws_route_table_association" "private-subnet-2-association" {
  route_table_id = aws_route_table.private-route-table.id
  subnet_id      = aws_subnet.private-subnet-2.id
}

resource "aws_internet_gateway" "saintmtool-igw" {
  vpc_id = aws_vpc.saintmtool-vpc.id

  tags = {
    Name = "Saintmtool-IGW"
  }
}

resource "aws_route" "public-internet-gw-route" {
  route_table_id         = aws_route_table.public-route-table.id
  gateway_id             = aws_internet_gateway.saintmtool-igw.id
  destination_cidr_block = "0.0.0.0/0"
}

resource "aws_alb" "saintmtool-alb" {
  name                             = var.saintmtool-alb
  load_balancer_type               = "application"
  subnets                          = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
  enable_cross_zone_load_balancing = true

  tags = {
    Name = var.saintmtool-alb
  }
}

resource "aws_alb_listener" "saintmtool-alb-listener" {
  load_balancer_arn = aws_alb.saintmtool-alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.saintmtool-web-app-tg.arn
  }
}

resource "aws_lb_target_group" "saintmtool-web-app-tg" {
  port                          = 80
  protocol                      = "HTTP"
  vpc_id                        = aws_vpc.saintmtool-vpc.id
  load_balancing_algorithm_type = "least_outstanding_requests"
}

resource "aws_acm_certificate" "saintmtool-domain-certificate" {
  domain_name       = var.saintmtool-domain
  validation_method = "DNS"
  subject_alternative_names = [
    "api-v1.${var.saintmtool-domain}"
  ]

  tags = {
    Name = "Saintmtool-Certificate"
  }
}

data "aws_route53_zone" "saintmtool-domain" {
  name         = var.saintmtool-domain
  private_zone = false
}

resource "aws_route53_record" "saintmtool-cert-validation-record" {
  for_each = {
    for dvo in aws_acm_certificate.saintmtool-domain-certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.saintmtool-domain.zone_id
}

resource "aws_acm_certificate_validation" "saintmtool-domain-certificate-validation" {
  certificate_arn         = aws_acm_certificate.saintmtool-domain-certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.saintmtool-cert-validation-record : record.fqdn]
}

resource "aws_launch_template" "saintmtool-launch-template" {
  name_prefix   = "saintmtool-lt"
  instance_type = "t3.micro"
  image_id      = "ami-1a2b3c"
  cpu_options {
    core_count       = 1
    threads_per_core = 2
  }
}

resource "aws_autoscaling_group" "saintmtool-autoscaling-group" {
  desired_capacity    = 1
  max_size            = 1
  min_size            = 1
  vpc_zone_identifier = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]

  launch_template {
    id      = aws_launch_template.saintmtool-launch-template.id
    version = "$Latest"
  }
}