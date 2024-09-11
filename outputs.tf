output "start_composition_webhook_url" {
  value = var.webhooks.deploy ? "${aws_api_gateway_stage.webhooks[0].invoke_url}/start" : null
}

output "stop_composition_webhook_url" {
  value = var.webhooks.deploy ? "${aws_api_gateway_stage.webhooks[0].invoke_url}/stop" : null
}

output "webhook_api_key" {
  value = var.webhooks.deploy ? aws_api_gateway_api_key.webhooks[0].value : null
}

output "api_gateway_stage_arn" {
  value = var.webhooks.deploy ? aws_api_gateway_stage.webhooks[0].arn : null
}
