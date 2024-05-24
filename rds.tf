locals {
  # Converts a RDS cluster/instance Maintenance Window (day:hour:minute-day:hour:minute)
  # to an extended cron expression. This makes sure a cluster/instance is up- and running
  # within its maintenance periods.

  rds_extend_by_minutes = 15

  rds_cluster_maintenance_windows = {
    for resource in var.resource_composition :
    resource.params["id"] => data.aws_rds_cluster.managed[resource.params["id"]].preferred_maintenance_window
    if resource.type == "rds_cluster"
  }
  rds_cluster_extended_maintenance_windows = {
    for cluster_id, preferred_window in local.rds_cluster_maintenance_windows :
    cluster_id => jsondecode(data.aws_lambda_invocation.rds_cluster_maintenance_windows[cluster_id].result)
  }

  rds_cluster_backup_windows = {
    for resource in var.resource_composition :
    resource.params["id"] => data.aws_rds_cluster.managed[resource.params["id"]].preferred_backup_window
    if resource.type == "rds_cluster"
  }
  rds_cluster_extended_backup_windows = {
    for cluster_id, preferred_window in local.rds_cluster_backup_windows :
    cluster_id => jsondecode(data.aws_lambda_invocation.rds_cluster_backup_windows[cluster_id].result)
  }

  rds_instance_maintenance_windows = {
    for resource in var.resource_composition :
    resource.params["id"] => data.aws_db_instance.managed[resource.params["id"]].preferred_maintenance_window
    if resource.type == "rds_instance"
  }
  rds_instance_extended_maintenance_windows = {
    for cluster_id, preferred_window in local.rds_instance_maintenance_windows :
    cluster_id => jsondecode(data.aws_lambda_invocation.rds_instance_maintenance_windows[cluster_id].result)
  }

  rds_instance_backup_windows = {
    for resource in var.resource_composition :
    resource.params["id"] => data.aws_db_instance.managed[resource.params["id"]].preferred_backup_window
    if resource.type == "rds_instance"
  }
  rds_instance_extended_backup_windows = {
    for cluster_id, preferred_window in local.rds_instance_backup_windows :
    cluster_id => jsondecode(data.aws_lambda_invocation.rds_instance_backup_windows[cluster_id].result)
  }
}

data "aws_rds_cluster" "managed" {
  for_each           = toset([for resource in var.resource_composition : resource.params["id"] if resource.type == "rds_cluster"])
  cluster_identifier = each.key
}

data "aws_db_instance" "managed" {
  for_each               = toset([for resource in var.resource_composition : resource.params["id"] if resource.type == "rds_instance"])
  db_instance_identifier = each.key
}

data "aws_lambda_invocation" "rds_cluster_maintenance_windows" {
  for_each = local.rds_cluster_maintenance_windows

  function_name = module.scheduler_lambda.name

  input = jsonencode({
    "resource_type" : "cron_helper",
    "action" : "extend_windows",
    "cron_helper_params" : {
      "aws_window_expression" : each.value,
      "minutes" : local.rds_extend_by_minutes,
      "start_resources_at" : var.start_resources_at,
      "stop_resources_at" : var.stop_resources_at,
      "timezone" : var.timezone
    }
  })

  depends_on = [module.scheduler_lambda]
}

data "aws_lambda_invocation" "rds_cluster_backup_windows" {
  for_each = local.rds_cluster_backup_windows

  function_name = module.scheduler_lambda.name

  input = jsonencode({
    "resource_type" : "cron_helper",
    "action" : "extend_windows",
    "cron_helper_params" : {
      "aws_window_expression" : each.value,
      "minutes" : local.rds_extend_by_minutes,
      "start_resources_at" : var.start_resources_at,
      "stop_resources_at" : var.stop_resources_at,
      "timezone" : var.timezone
    }
  })

  depends_on = [module.scheduler_lambda]
}

data "aws_lambda_invocation" "rds_instance_maintenance_windows" {
  for_each = local.rds_instance_maintenance_windows

  function_name = module.scheduler_lambda.name

  input = jsonencode({
    "resource_type" : "cron_helper",
    "action" : "extend_windows",
    "cron_helper_params" : {
      "aws_window_expression" : each.value,
      "minutes" : local.rds_extend_by_minutes,
      "start_resources_at" : var.start_resources_at,
      "stop_resources_at" : var.stop_resources_at,
      "timezone" : var.timezone
    }
  })

  depends_on = [module.scheduler_lambda]
}

data "aws_lambda_invocation" "rds_instance_backup_windows" {
  for_each = local.rds_instance_backup_windows

  function_name = module.scheduler_lambda.name

  input = jsonencode({
    "resource_type" : "cron_helper",
    "action" : "extend_windows",
    "cron_helper_params" : {
      "aws_window_expression" : each.value,
      "minutes" : local.rds_extend_by_minutes,
      "start_resources_at" : var.start_resources_at,
      "stop_resources_at" : var.stop_resources_at,
      "timezone" : var.timezone
    }
  })

  depends_on = [module.scheduler_lambda]
}
