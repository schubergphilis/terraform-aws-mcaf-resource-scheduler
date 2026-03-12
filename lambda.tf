locals {
  resource_types_in_composition = distinct([
    for resource in var.resource_composition : resource.type
  ])
}

data "archive_file" "scheduler_source" {
  type        = "zip"
  source_dir  = "${path.module}/scheduler"
  output_path = "scheduler.zip"
}

module "scheduler_lambda" {
  source  = "schubergphilis/mcaf-lambda/aws"
  version = "~> 3.0.0"

  #checkov:skip=CKV_AWS_338:Ensure CloudWatch log groups retains logs for at least 1 year
  filename         = data.archive_file.scheduler_source.output_path
  source_code_hash = data.archive_file.scheduler_source.output_base64sha256

  name          = "resource-scheduler-${var.composition_name}"
  description   = "Resource Scheduler Lambda Function"
  handler       = "scheduler.scheduler.handler"
  kms_key_arn   = var.kms_key_arn
  log_retention = 90
  memory_size   = 256
  retries       = 0
  runtime       = "python3.13"
  timeout       = 60

  environment = {
    POWERTOOLS_LOG_LEVEL    = "INFO"
    POWERTOOLS_SERVICE_NAME = "composition-scheduler-${var.composition_name}"
  }

  execution_role_custom = {
    arn = module.lambda_role.arn
  }

  # Use a AWS provided layer to include Powertools to simplify redistribution.
  # Also see https://docs.powertools.aws.dev/lambda/python/latest/#lambda-layer.
  layers = [
    "arn:aws:lambda:${data.aws_region.current.name}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-x86_64:27"
  ]

  tags = var.tags
}
