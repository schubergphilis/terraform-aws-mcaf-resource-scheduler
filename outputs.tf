output "start_stack_webhook_url" {
  value = var.webhooks.deploy ? "${aws_api_gateway_stage.webhooks[0].invoke_url}/start" : null
}

output "stop_stack_webhook_url" {
  value = var.webhooks.deploy ? "${aws_api_gateway_stage.webhooks[0].invoke_url}/stop" : null
}

output "webhook_api_key" {
  value = var.webhooks.deploy ? aws_api_gateway_api_key.webhooks[0].value : null
}
