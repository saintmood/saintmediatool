output "vpc_id" {
  value = aws_vpc.saintmtool_vpc.id
}

output "vpc_cidr_block" {
  value = aws_vpc.saintmtool_vpc.cidr_block
}
