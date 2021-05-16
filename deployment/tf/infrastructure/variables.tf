variable "aws-region" {
  type    = string
  default = "eu-west-1"
}

variable "vpc_cidr" {
  description = "Saintmtool VPC Cidr Block"
}

variable "public_subnet_1_cidr" {
  description = "Public Saintmtool Subnet 1 Cidr"
}

variable "public_subnet_2_cidr" {
  description = "Public Saintmtool Subnet 2 Cidr"
}

variable "private_subnet_1_cidr" {
  description = "Private Saintmtool Subnet 1 Cidr"
}

variable "private_subnet_2_cidr" {
  description = "Private Saintmtool Subnet 2 Cidr"
}

variable "saintmtool-alb" {
  default = "saintmtool-alb"
  type    = string
}

variable "saintmtool-domain" {
  type    = string
  default = "saintmtool.net"
}