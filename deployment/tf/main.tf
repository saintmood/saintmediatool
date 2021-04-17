terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~>2.11.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "saintmtool" {
  name = "saintmtool:latest"
}

resource "docker_container" "saintmtool" {
  image = "docker_image.saintmtool.latest"
  name = "saintmtool"
}