terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 3.64.2"
    }
  }
}

provider "aws" {
  region = var.aws_region
  profile = var.aws_profile

  default_tags {
    tags = {
      Terraform = "true"
      Project = "saintmediatool"
    }
  }
}
