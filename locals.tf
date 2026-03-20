locals {
  account_region = var.region != null ? var.region : data.aws_region.current.region
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
