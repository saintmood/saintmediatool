variable "env" {
  description = "Env to deploy to"
  type = string
  default = "dev"
}

variable "image" {
  description = "Container Image to use"
  type = map
  default = {
    dev = "sainmtool-dev"
    prod = "saintmtool-prod"
  }
}