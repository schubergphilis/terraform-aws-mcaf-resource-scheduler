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
    condition     = length([for r in var.resource_composition : r if contains(["ec2_instance", "rds_instance", "rds_cluster", "auto_scaling_group", "ecs_service", "redshift_cluster", "wait"], r.type)]) == length(var.resource_composition)
    error_message = "Resource type must be one of ec2_instance, rds_instance, rds_cluster, auto_scaling_group, ecs_service or redshift_cluster"
  }
}

variable "webhooks" {
  type = object({
    deploy       = bool
    ip_whitelist = list(string)
    private      = optional(bool, false)
  })
  default = {
    deploy       = false
    ip_whitelist = []
    private      = false
  }
  description = "Deploy webhooks for external triggers"
}

variable "composition_name" {
  type        = string
  description = "The name of the controlled composition"
}

variable "start_resources_at" {
  type        = string
  description = "Resources start cron expression in selected timezone"

  validation {
    condition     = var.start_resources_at == "on-demand" || length(split(" ", var.start_resources_at)) == 6
    error_message = "Start resources at must be on-demand or a valid cron expression."
  }
}

variable "stop_resources_at" {
  type        = string
  description = "Resources stop cron expression in selected timezone"

  validation {
    condition     = var.stop_resources_at == "on-demand" || length(split(" ", var.stop_resources_at)) == 6
    error_message = "Stop resources at must be on-demand or a valid cron expression."
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
  default     = "UTC"
}
