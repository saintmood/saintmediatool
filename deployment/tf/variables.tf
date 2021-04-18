variable "env" {
  description = "Env to deploy to"
  type = string
  default = "dev"
}

variable "ext_port" {
  type = list
}

variable "image" {
  description = "Container Image to use"
  type = map
  default = {
    dev = "sainmtool-dev"
    prod = "saintmtool-prod"
  }
}

locals {
  container_count = length(var.ext_port)
}