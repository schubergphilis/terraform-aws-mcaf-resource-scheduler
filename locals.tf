locals {
  account_region = var.region != null ? var.region : data.aws_region.current.region
}
