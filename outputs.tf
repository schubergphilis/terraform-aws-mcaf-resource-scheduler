output "api_gateway_id" {
  value       = var.webhooks.deploy ? aws_api_gateway_rest_api.webhooks[0].id : null
  description = "The ID of the API Gateway used by the webhooks (if webhooks are enabled)"
}

output "api_gateway_stage_arn" {
  value       = var.webhooks.deploy ? aws_api_gateway_stage.webhooks[0].arn : null
  description = "The ARN of the API Gateway stage used by the webhooks (if webhooks are enabled)"
}

output "start_composition_state_machine_arn" {
  value       = aws_sfn_state_machine.composition_start.arn
  description = "The ARN of the Step Functions state machine used to start the composition"
}

output "start_composition_webhook_url" {
  value       = var.webhooks.deploy ? "${aws_api_gateway_stage.webhooks[0].invoke_url}/start" : null
  description = "The webhook URL used to start the composition (if webhooks are enabled)"
}

output "stop_composition_state_machine_arn" {
  value       = aws_sfn_state_machine.composition_stop.arn
  description = "The ARN of the Step Functions state machine used to stop the composition"
}

output "stop_composition_webhook_url" {
  value       = var.webhooks.deploy ? "${aws_api_gateway_stage.webhooks[0].invoke_url}/stop" : null
  description = "The webhook URL used to stop the composition (if webhooks are enabled)"
}

output "webhook_api_key" {
  value       = var.webhooks.deploy ? aws_api_gateway_api_key.webhooks[0].value : null
  description = "The API key used to authenticate requests to any the webhooks (if webhooks are enabled)"
}
