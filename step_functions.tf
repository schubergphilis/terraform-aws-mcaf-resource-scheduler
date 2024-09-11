locals {
  composition_state_done = { "Done" : { "Type" : "Succeed" } }

  start_composition_states_resources = {
    for index, resource in var.resource_composition : "Step${index + 1}" => [{
      "Type" : "Wait",
      "Seconds" : resource.type == "wait" ? tonumber(resource.params["seconds"]) : 0,
      "Next" : "Step${index + 2}"
      }, {
      "Type" : "Task",
      "Resource" : module.scheduler_lambda.arn,
      "Parameters" : {
        "action" : "start",
        "resource_type" : resource.type,
        "${resource.type}_params" : resource.params
      },
      "Next" : ((index + 1) == length(var.resource_composition)) ? "Done" : "Step${index + 2}"
    }][resource.type == "wait" ? 0 : 1]
  }

  start_composition_states = merge(local.start_composition_states_resources, local.composition_state_done)

  stop_composition_states_resources = {
    for index, resource in reverse(var.resource_composition) : "Step${index + 1}" => [{
      "Type" : "Wait",
      "Seconds" : resource.type == "wait" ? tonumber(resource.params["seconds"]) : 0,
      "Next" : "Step${index + 2}"
      }, {
      "Type" : "Task",
      "Resource" : module.scheduler_lambda.arn,
      "Parameters" : {
        "action" : "stop",
        "resource_type" : resource.type,
        "${resource.type}_params" : resource.params
      },
      "Next" : ((index + 1) == length(var.resource_composition)) ? "Done" : "Step${index + 2}"
    }][resource.type == "wait" ? 0 : 1]
  }

  stop_composition_states = merge(local.stop_composition_states_resources, local.composition_state_done)
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_sfn_state_machine" "composition_start" {
  #checkov:skip=CKV_AWS_284
  #checkov:skip=CKV_AWS_285:Logging is only valid for express workflows
  name     = "composition-scheduler-start-${var.composition_name}"
  role_arn = module.step_functions_role.arn
  tags     = var.tags

  definition = templatefile("${path.module}/templates/sfn_start_composition.json.tpl", {
    composition_name = var.composition_name
    states           = jsonencode(local.start_composition_states)
  })
}

resource "aws_sfn_state_machine" "composition_stop" {
  #checkov:skip=CKV_AWS_284
  #checkov:skip=CKV_AWS_285:Logging is only valid for express workflows
  name     = "composition-scheduler-stop-${var.composition_name}"
  role_arn = module.step_functions_role.arn
  tags     = var.tags

  definition = templatefile("${path.module}/templates/sfn_stop_composition.json.tpl", {
    composition_name = var.composition_name
    states           = jsonencode(local.stop_composition_states)
  })
}
