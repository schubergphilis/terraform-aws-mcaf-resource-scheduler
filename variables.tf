variable "kms_key_arn" {
  description = "The ARN of the KMS key to use with the Lambda function"
  type        = string
}

variable "resource_composition" {
  type = list(object({
    type   = string
    params = map(any)
  }))
  description = "Resource composition"

  validation {
    condition     = length([for r in var.resource_composition : r if contains(["rds_instance", "rds_cluster", "auto_scaling_group", "ecs_service", "redshift_cluster", "wait"], r.type)]) == length(var.resource_composition)
    error_message = "Resource type must be one of rds_instance, rds_cluster, auto_scaling_group, ecs_service or redshift_cluster"
  }
}

variable "self_service_configuration" {
  type = object({
    enabled = bool
    private = bool
  })

  default = {
    enabled = false
    private = true
  }

  description = "Self-service portal configuration"
}

variable "stack_name" {
  type        = string
  description = "The name of the controlled stack"
}

variable "start_stack_at" {
  type        = string
  description = "Stack start expression"

  validation {
    condition     = var.start_stack_at == "on-demand" || length(split(" ", var.start_stack_at)) == 6
    error_message = "Start stack at must be on-demand or a valid cron expression."
  }
}

variable "stop_stack_at" {
  type        = string
  description = "Stack stop expression"

  validation {
    condition     = var.stop_stack_at == "on-demand" || length(split(" ", var.stop_stack_at)) == 6
    error_message = "Stop stack at must be on-demand or a valid cron expression."
  }
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Mapping of tags"
}

variable "timezone" {
  type        = string
  description = "Timezone to execute schedules in"
  default     = "Europe/Amsterdam"
}
