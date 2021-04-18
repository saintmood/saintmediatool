terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~>2.11.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}
provider "aws" {
  region = "us-east-1"
}


resource "docker_image" "saintmtool" {
  name = lookup(var.image, var.env)
}

resource "docker_container" "saintmtool" {
  image = "docker_image.saintmtool.latest"
  name = "saintmtool"
}