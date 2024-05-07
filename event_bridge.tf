resource "aws_scheduler_schedule_group" "scheduler" {
  name = "stack-scheduler-${var.stack_name}"
  tags = var.tags
}

resource "aws_scheduler_schedule" "start_stack" {
  count = var.start_stack_at == "on-demand" ? 0 : 1

  name                         = "${var.stack_name}-start"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${var.start_stack_at})"
  schedule_expression_timezone = var.timezone
  state                        = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:sfn:startExecution"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      Input           = jsonencode({}),
      StateMachineArn = aws_sfn_state_machine.stack_start.arn,
    })
  }
}

resource "aws_scheduler_schedule" "stop_stack" {
  count = var.stop_stack_at == "on-demand" ? 0 : 1

  name                         = "${var.stack_name}-stop"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${var.stop_stack_at})"
  schedule_expression_timezone = var.timezone
  state                        = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:sfn:startExecution"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      Input           = jsonencode({}),
      StateMachineArn = aws_sfn_state_machine.stack_stop.arn,
    })
  }
}

resource "aws_scheduler_schedule" "redshift_cluster_maintenance_start" {
  for_each = local.redshift_cluster_extended_maintenance_windows

  name                         = "schedule-${var.stack_name}-redshift-cluster-maint-start-${index(keys(local.redshift_cluster_extended_maintenance_windows), each.key)}"
  description                  = "Start Redshift cluster ${each.key} for start of maintenance window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["start"]})"
  schedule_expression_timezone = "UTC" # Redshift maintenance is in UTC
  state                        = each.value["skip_start"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "start",
        "resource_type" : "redshift_cluster",
        "redshift_cluster_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "redshift_cluster_maintenance_stop" {
  for_each = local.redshift_cluster_extended_maintenance_windows

  name                         = "schedule-${var.stack_name}-redshift-cluster-maint-stop-${index(keys(local.redshift_cluster_extended_maintenance_windows), each.key)}"
  description                  = "Stop Redshift cluster ${each.key} for end of maintenance window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["stop"]})"
  schedule_expression_timezone = "UTC" # Redshift maintenance is in UTC
  state                        = each.value["skip_stop"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "stop",
        "resource_type" : "redshift_cluster",
        "redshift_cluster_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_cluster_maintenance_start" {
  for_each = local.rds_cluster_extended_maintenance_windows

  name                         = "schedule-${var.stack_name}-rds-cluster-maint-start-${index(keys(local.rds_cluster_extended_maintenance_windows), each.key)}"
  description                  = "Start RDS cluster ${each.key} for start of maintenance window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["start"]})"
  schedule_expression_timezone = "UTC" # RDS maintenance is in UTC
  state                        = each.value["skip_start"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "start",
        "resource_type" : "rds_cluster",
        "rds_cluster_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_cluster_maintenance_stop" {
  for_each = local.rds_cluster_extended_maintenance_windows

  name                         = "schedule-${var.stack_name}-rds-cluster-maint-stop-${index(keys(local.rds_cluster_extended_maintenance_windows), each.key)}"
  description                  = "Stop RDS cluster ${each.key} for end of maintenance window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["stop"]})"
  schedule_expression_timezone = "UTC" # RDS maintenance is in UTC
  state                        = each.value["skip_stop"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "stop",
        "resource_type" : "rds_cluster",
        "rds_cluster_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_cluster_backup_start" {
  for_each = local.rds_cluster_extended_backup_windows

  name                         = "schedule-${var.stack_name}-rds-cluster-backup-start-${index(keys(local.rds_cluster_extended_backup_windows), each.key)}"
  description                  = "Start RDS cluster ${each.key} for start of backup window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["start"]})"
  schedule_expression_timezone = "UTC" # RDS maintenance is in UTC
  state                        = each.value["skip_start"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "start",
        "resource_type" : "rds_cluster",
        "rds_cluster_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_cluster_backup_stop" {
  for_each = local.rds_cluster_extended_backup_windows

  name                         = "schedule-${var.stack_name}-rds-cluster-backup-stop-${index(keys(local.rds_cluster_extended_backup_windows), each.key)}"
  description                  = "Stop RDS cluster ${each.key} for end of backup window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["stop"]})"
  schedule_expression_timezone = "UTC" # RDS maintenance is in UTC
  state                        = each.value["skip_stop"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "stop",
        "resource_type" : "rds_cluster",
        "rds_cluster_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_instance_maintenance_start" {
  for_each = local.rds_instance_extended_maintenance_windows

  name                         = "schedule-${var.stack_name}-rds-instance-maint-start-${index(keys(local.rds_instance_extended_maintenance_windows), each.key)}"
  description                  = "Start RDS instance ${each.key} for start of maintenance window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["start"]})"
  schedule_expression_timezone = "UTC" # RDS maintenance is in UTC
  state                        = each.value["skip_start"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "start",
        "resource_type" : "rds_instance",
        "rds_instance_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_instance_maintenance_stop" {
  for_each = local.rds_instance_extended_maintenance_windows

  name                         = "schedule-${var.stack_name}-rds-instance-maint-stop-${index(keys(local.rds_instance_extended_maintenance_windows), each.key)}"
  description                  = "Stop RDS instance ${each.key} for end of maintenance window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["stop"]})"
  schedule_expression_timezone = "UTC" # RDS maintenance is in UTC
  state                        = each.value["skip_stop"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "stop",
        "resource_type" : "rds_insta ce",
        "rds_instance_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_instance_backup_start" {
  for_each = local.rds_instance_extended_backup_windows

  name                         = "schedule-${var.stack_name}-rds-instance-backup-start-${index(keys(local.rds_instance_extended_backup_windows), each.key)}"
  description                  = "Start RDS instance ${each.key} for start of backup window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["start"]})"
  schedule_expression_timezone = "UTC" # RDS backup window is in UTC
  state                        = each.value["skip_start"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "start",
        "resource_type" : "rds_instance",
        "rds_instance_params" : {
          "id" : each.key
        }
      })
    })
  }
}

resource "aws_scheduler_schedule" "rds_instance_backup_stop" {
  for_each = local.rds_instance_extended_backup_windows

  name                         = "schedule-${var.stack_name}-rds-instance-backup-stop-${index(keys(local.rds_instance_extended_backup_windows), each.key)}"
  description                  = "Stop RDS instance ${each.key} for end of backup window"
  group_name                   = aws_scheduler_schedule_group.scheduler.name
  schedule_expression          = "cron(${each.value["stop"]})"
  schedule_expression_timezone = "UTC" # RDS backup window is in UTC
  state                        = each.value["skip_stop"] == false ? "ENABLED" : "DISABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:lambda:invoke"
    role_arn = module.eventbridge_scheduler_role.arn

    input = jsonencode({
      FunctionName   = module.scheduler_lambda.arn,
      InvocationType = "Event",
      Payload = jsonencode({
        "action" : "stop",
        "resource_type" : "rds_instance",
        "rds_instance_params" : {
          "id" : each.key
        }
      })
    })
  }
}
