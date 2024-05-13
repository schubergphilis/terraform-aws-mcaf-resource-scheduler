terraform {
  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.10.0"
    }
  }

  required_version = ">= 1.5.0"
}
