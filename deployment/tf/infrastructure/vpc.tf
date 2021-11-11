resource "aws_vpc" "saintmtool_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "Saintmtool-VPC"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_internet_gateway" "saintmtool_igw" {
  vpc_id = aws_vpc.saintmtool_vpc.id

  tags = {
    Name = "Saintmtool-IGW"
  }
}


data "aws_availability_zones" "available_azs" {
  state = "available"
}

resource "aws_subnet" "public_subnets" {
  for_each = var.public_subnets

  vpc_id = aws_vpc.saintmtool_vpc.id
  availability_zone = [
    for az in data.aws_availability_zones.available_azs.names :
    az
    if substr(az, -1, -1) == each.value.az_letter
  ][0]
  cidr_block = each.value.cidr
  tags = {
    Name = "Public-Subnet-${each.value.az_letter}"
    Type = "Public"
  }
}

resource "aws_subnet" "private_subnets" {
  for_each = var.private_subnets

  vpc_id = aws_vpc.saintmtool_vpc.id
  availability_zone = [
    for az in data.aws_availability_zones.available_azs.names :
    az
    if substr(az, -1, -1) == each.value.az_letter
  ][0]
  cidr_block = each.value.cidr
  tags = {
    Name = "Private-Subnet-${each.value.az_letter}"
    Type = "Private"
  }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.saintmtool_vpc.id
  tags = {
    Name = "Public-Route-Table"
  }
}

resource "aws_route" "igw_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.saintmtool_igw.id
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.saintmtool_vpc.id
  tags = {
    Name = "Private-Route-Table"
  }
}

resource "aws_route_table_association" "public_subnets" {
  for_each = var.public_subnets

  route_table_id = aws_route_table.public_route_table.id
  subnet_id      = aws_subnet.public_subnets[each.key].id
}

resource "aws_route_table_association" "private_subnets" {
  for_each = var.private_subnets

  route_table_id = aws_route_table.private_route_table.id
  subnet_id      = aws_subnet.private_subnets[each.key].id
}

resource "aws_alb" "saintmtool_alb" {
  name               = var.saintmtool_alb
  load_balancer_type = "application"
  subnets = [
    for subnet in aws_subnet.public_subnets :
    subnet.id
  ]
  enable_cross_zone_load_balancing = true

  tags = {
    Name = var.saintmtool_alb
  }
}

resource "aws_alb_listener" "saintmtool_alb_listener" {
  load_balancer_arn = aws_alb.saintmtool_alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.saintmtool_domain_certificate.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.saintmtool_web_app_tg.arn
  }

  depends_on = [
    aws_alb_target_group.saintmtool_web_app_tg
  ]
}

resource "aws_alb_target_group" "saintmtool_web_app_tg" {
  name                          = "sainmtool-webapp-tg"
  port                          = 80
  protocol                      = "HTTP"
  vpc_id                        = aws_vpc.saintmtool_vpc.id
  load_balancing_algorithm_type = "least_outstanding_requests"

  tags = {
    Name = "Saintmtool-Webapp-TG"
  }
}

resource "aws_acm_certificate" "saintmtool_domain_certificate" {
  domain_name       = var.saintmtool_domain
  validation_method = "DNS"
  subject_alternative_names = [
    "api-v1.${var.saintmtool_domain}"
  ]

  tags = {
    Name = "Saintmtool-Certificate"
  }
}

data "aws_route53_zone" "saintmtool_domain" {
  name         = var.saintmtool_domain
  private_zone = false
}

resource "aws_route53_record" "saintmtool-cert-validation-record" {
  for_each = {
    for dvo in aws_acm_certificate.saintmtool_domain_certificate.domain_validation_options : dvo.domain_name => {
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
  zone_id         = data.aws_route53_zone.saintmtool_domain.zone_id
}

resource "aws_acm_certificate_validation" "saintmtool_domain_certificate_validation" {
  certificate_arn         = aws_acm_certificate.saintmtool_domain_certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.saintmtool-cert-validation-record : record.fqdn]
}

resource "aws_route53_record" "saintmtool_alb_record" {
  name    = var.saintmtool_domain
  type    = "A"
  zone_id = data.aws_route53_zone.saintmtool_domain.zone_id

  alias {
    evaluate_target_health = false
    name                   = aws_alb.saintmtool_alb.dns_name
    zone_id                = aws_alb.saintmtool_alb.zone_id
  }
}

resource "aws_launch_template" "saintmtool_launch_template" {
  name_prefix   = "saintmtool-lt-"
  instance_type = var.instance_type
  image_id      = var.instance_ami_id
  cpu_options {
    core_count       = 1
    threads_per_core = 2
  }
  user_data = var.instance_user_data_script
}

resource "aws_autoscaling_group" "saintmtool_autoscaling_group" {
  desired_capacity = 1
  max_size         = 1
  min_size         = 1
  vpc_zone_identifier = [
    for subnet in aws_subnet.public_subnets :
    subnet.id
  ]
  target_group_arns = [
    aws_alb_target_group.saintmtool_web_app_tg.arn,
  ]

  launch_template {
    id      = aws_launch_template.saintmtool_launch_template.id
    version = "$Latest"
  }
}
