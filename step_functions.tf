locals {
  start_stack_states_resources = {
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

  start_stack_states = merge(
    {
      "Done" : { "Type" : "Succeed" }
    },
    local.start_stack_states_resources,
  )

  stop_stack_states_resources = {
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

  stop_stack_states = merge(
    {
      "Done" : { "Type" : "Succeed" }
    },
    local.stop_stack_states_resources
  )
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_sfn_state_machine" "stack_start" {
  name     = "stack-scheduler-control-machine-start-${var.stack_name}"
  role_arn = module.step_functions_role.arn
  tags     = var.tags

  definition = templatefile("${path.module}/templates/start_stack.tpl.json", {
    stack_name = var.stack_name
    states     = jsonencode(local.start_stack_states)
  })
}

resource "aws_sfn_state_machine" "stack_stop" {
  name     = "stack-scheduler-control-machine-stop-${var.stack_name}"
  role_arn = module.step_functions_role.arn
  tags     = var.tags

  definition = templatefile("${path.module}/templates/stop_stack.tpl.json", {
    stack_name = var.stack_name
    states     = jsonencode(local.stop_stack_states)
  })
}
