resource "aws_api_gateway_rest_api" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  name = "composition-scheduler-webhooks-${var.composition_name}"

  endpoint_configuration {
    types = var.webhooks.private ? ["PRIVATE"] : ["REGIONAL"]
  }

  tags = var.tags
}

resource "aws_api_gateway_deployment" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id

  depends_on = [
    aws_api_gateway_integration.webhook_start_composition[0],
    aws_api_gateway_integration.webhook_stop_composition[0],
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "webhooks" {
  #checkov:skip=CKV2_AWS_29:The API Gateway can be IP whitelisted. The stage ARN is part of the output for users to setup their own WAF outside of this module if desired.
  #checkov:skip=CKV2_AWS_51
  count = var.webhooks.deploy ? 1 : 0

  deployment_id = aws_api_gateway_deployment.webhooks[0].id
  rest_api_id   = aws_api_gateway_rest_api.webhooks[0].id
  stage_name    = "default"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.webhooks[0].arn
    format          = "{ \"requestId\":\"$context.requestId\", \"ip\": \"$context.identity.sourceIp\", \"caller\":\"$context.identity.caller\", \"user\":\"$context.identity.user\",\"requestTime\":\"$context.requestTime\", \"httpMethod\":\"$context.httpMethod\",\"resourcePath\":\"$context.resourcePath\", \"status\":\"$context.status\",\"protocol\":\"$context.protocol\", \"responseLength\":\"$context.responseLength\" }"
  }

  tags = var.tags

  depends_on = [
    aws_cloudwatch_log_group.webhooks[0]
  ]
}

resource "aws_api_gateway_method_settings" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  stage_name  = aws_api_gateway_stage.webhooks[0].stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}

resource "aws_cloudwatch_log_group" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  name              = "API-Gateway-composition-scheduler-${var.composition_name}/default"
  kms_key_id        = var.kms_key_arn
  retention_in_days = 90
  tags              = var.tags
}

resource "aws_api_gateway_usage_plan" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  name = "composition-scheduler-webhooks-${var.composition_name}-usage-plan"
  tags = var.tags

  api_stages {
    api_id = aws_api_gateway_rest_api.webhooks[0].id
    stage  = aws_api_gateway_stage.webhooks[0].stage_name
  }
}

resource "aws_api_gateway_api_key" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  name = "composition-scheduler-webhooks-${var.composition_name}-api-key"
  tags = var.tags
}

resource "aws_api_gateway_usage_plan_key" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  key_id        = aws_api_gateway_api_key.webhooks[0].id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.webhooks[0].id
}

resource "aws_api_gateway_rest_api_policy" "webhooks" {
  count = var.webhooks.deploy && length(var.webhooks.ip_whitelist) > 0 ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : [
            "execute-api:Invoke"
          ],
          "Principal" : {
            "AWS" : "*"
          },
          "Resource" : "${aws_api_gateway_rest_api.webhooks[0].execution_arn}/${aws_api_gateway_stage.webhooks[0].stage_name}/*/*",
          "Effect" : "Allow",
          "Condition" : {
            "IpAddress" : {
              "aws:SourceIp" : var.webhooks.ip_whitelist
            }
          }
        }
      ]
    }
  )
}

resource "aws_api_gateway_model" "webhooks" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id  = aws_api_gateway_rest_api.webhooks[0].id
  name         = "StepFunctionExecutionResponseModel"
  description  = "API response for Step Function execution response"
  content_type = "application/json"
  schema = jsonencode({
    "$schema" = "http://json-schema.org/draft-04/schema#"
    title     = "StepFunctionExecutionResponse"
    type      = "object"
    properties = {
      executionArn = {
        type = "string"
      },
      "startDate" = {
        type = "number"
      }
    }
  })
}

##################################################
# /start
##################################################

resource "aws_api_gateway_resource" "webhook_start_composition" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  parent_id   = aws_api_gateway_rest_api.webhooks[0].root_resource_id
  path_part   = "start"
}

resource "aws_api_gateway_method" "webhook_start_composition" {
  #checkov:skip=CKV2_AWS_53:These webhooks take no parameters or request body to validate
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id      = aws_api_gateway_rest_api.webhooks[0].id
  resource_id      = aws_api_gateway_resource.webhook_start_composition[0].id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_integration" "webhook_start_composition" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id             = aws_api_gateway_rest_api.webhooks[0].id
  resource_id             = aws_api_gateway_resource.webhook_start_composition[0].id
  http_method             = aws_api_gateway_method.webhook_start_composition[0].http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${data.aws_region.current.name}:states:action/StartExecution"
  credentials             = module.api_gateway_role[0].arn

  request_templates = {
    "application/json" = <<EOF
{
  "input": "{}",
  "stateMachineArn": "${aws_sfn_state_machine.composition_start.arn}"
}
EOF
  }
}

resource "aws_api_gateway_method_response" "webhook_start_composition_200" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  resource_id = aws_api_gateway_resource.webhook_start_composition[0].id
  http_method = aws_api_gateway_method.webhook_start_composition[0].http_method
  status_code = "200"

  response_models = {
    "application/json" = aws_api_gateway_model.webhooks[0].name
  }
}

resource "aws_api_gateway_integration_response" "webhook_start_composition" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  resource_id = aws_api_gateway_resource.webhook_start_composition[0].id
  http_method = aws_api_gateway_method.webhook_start_composition[0].http_method
  status_code = aws_api_gateway_method_response.webhook_start_composition_200[0].status_code

  depends_on = [
    aws_api_gateway_integration.webhook_start_composition[0]
  ]
}

##################################################
# /stop
##################################################

resource "aws_api_gateway_resource" "webhook_stop_composition" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  parent_id   = aws_api_gateway_rest_api.webhooks[0].root_resource_id
  path_part   = "stop"
}

resource "aws_api_gateway_method" "webhook_stop_composition" {
  #checkov:skip=CKV2_AWS_53:These webhooks take no parameters or request body to validate
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id      = aws_api_gateway_rest_api.webhooks[0].id
  resource_id      = aws_api_gateway_resource.webhook_stop_composition[0].id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_integration" "webhook_stop_composition" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id             = aws_api_gateway_rest_api.webhooks[0].id
  resource_id             = aws_api_gateway_resource.webhook_stop_composition[0].id
  http_method             = aws_api_gateway_method.webhook_stop_composition[0].http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${data.aws_region.current.name}:states:action/StartExecution"
  credentials             = module.api_gateway_role[0].arn

  request_templates = {
    "application/json" = <<EOF
{
  "input": "{}",
  "stateMachineArn": "${aws_sfn_state_machine.composition_stop.arn}"
}
EOF
  }
}

resource "aws_api_gateway_method_response" "webhook_stop_composition_200" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  resource_id = aws_api_gateway_resource.webhook_stop_composition[0].id
  http_method = aws_api_gateway_method.webhook_stop_composition[0].http_method
  status_code = "200"

  response_models = {
    "application/json" = aws_api_gateway_model.webhooks[0].name
  }
}

resource "aws_api_gateway_integration_response" "webhook_stop_composition" {
  count = var.webhooks.deploy ? 1 : 0

  rest_api_id = aws_api_gateway_rest_api.webhooks[0].id
  resource_id = aws_api_gateway_resource.webhook_stop_composition[0].id
  http_method = aws_api_gateway_method.webhook_stop_composition[0].http_method
  status_code = aws_api_gateway_method_response.webhook_stop_composition_200[0].status_code

  depends_on = [
    aws_api_gateway_integration.webhook_stop_composition[0]
  ]
}
