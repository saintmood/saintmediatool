variable "aws_region" {
  type    = string
  default = "eu-west-1"
}

variable "aws_profile" {
  type        = string
  default     = "default"
  description = "Named AWS CLI profile"
}

variable "vpc_cidr" {
  type        = string
  description = "Saintmtool VPC Cidr Block"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 1))
    error_message = "Variable \"vpc_cidr\" must use CIDR notation."
  }
}

variable "public_subnets" {
  type = map(object({
    az_letter = string
    cidr      = string
  }))
  default     = {}
  description = "Map of public subnet objects"
}

variable "private_subnets" {
  type = map(object({
    az_letter = string
    cidr      = string
  }))
  default     = {}
  description = "Map of private subnet objects"
}

variable "saintmtool_alb" {
  type    = string
  default = "saintmtool-alb"
}

variable "saintmtool_domain" {
  type    = string
  default = "saintmtool.net"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "instance_ami_id" {
  type    = string
  default = "ami-1a2b3c"
}

variable "instance_user_data_script" {
  type    = string
  default = <<-EOSCRIPT
  #!/bin/bash

  echo "I'm the test user data"
  EOSCRIPT
}
