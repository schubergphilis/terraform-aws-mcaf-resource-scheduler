locals {
  # Converts a Redshift Maintenance Window (day:hour:minute-day:hour:minute)
  # to an extended cron expression. This makes sure a cluster is up- and running
  # within its maintenance periods.

  redshift_extend_by_minutes = 15

  redshift_cluster_maintenance_windows = {
    for resource in var.resource_composition :
    resource.params["id"] => data.aws_redshift_cluster.managed[resource.params["id"]].preferred_maintenance_window
    if resource.type == "redshift_cluster"
  }
  redshift_cluster_extended_maintenance_windows = {
    for cluster_id, preferred_window in local.redshift_cluster_maintenance_windows :
    cluster_id => jsondecode(data.aws_lambda_invocation.redshift_cluster_maintenance_windows[cluster_id].result)
  }
}

data "aws_redshift_cluster" "managed" {
  for_each           = toset([for resource in var.resource_composition : resource.params["id"] if resource.type == "redshift_cluster"])
  cluster_identifier = each.key
}

data "aws_lambda_invocation" "redshift_cluster_maintenance_windows" {
  for_each = local.redshift_cluster_maintenance_windows

  function_name = module.scheduler_lambda.name

  input = jsonencode({
    "resource_type" : "cron_helper",
    "action" : "extend_windows",
    "cron_helper_params" : {
      "aws_window_expression" : each.value,
      "minutes" : local.redshift_extend_by_minutes,
      "start_stack_at" : var.start_stack_at,
      "stop_stack_at" : var.stop_stack_at
    }
  })

  depends_on = [module.scheduler_lambda]
}
