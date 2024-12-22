variable "kms_key_arn" {
  description = "The ARN of the KMS key to use with the Lambda function"
  type        = string

  validation {
    condition     = can(regex("arn:aws:kms:[a-z0-9-]+:[0-9]+:key/[a-f0-9-]+", var.kms_key_arn))
    error_message = "KMS key ARN must be in the format arn:aws:kms:<region>:<account>:key/<key-id>"
  }
}

variable "resource_composition" {
  type = list(object({
    type   = string
    params = map(any)
  }))
  description = "Resource composition"

  validation {
    condition     = length([for r in var.resource_composition : r if contains(["ec2_instance", "rds_instance", "rds_cluster", "auto_scaling_group", "ecs_service", "redshift_cluster", "wait", "fsx_windows_file_system"], r.type)]) == length(var.resource_composition)
    error_message = "Resource type must be one of ec2_instance, rds_instance, rds_cluster, auto_scaling_group, ecs_service, redshift_cluster or fsx_windows_file_system"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "auto_scaling_group" ? keys(r.params) == tolist(["desired", "max", "min", "name"]) : true)], false)
    error_message = "Auto-scaling group resources must have 'desired', 'max', 'min' and 'name' parameters"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "ec2_instance" ? keys(r.params) == tolist(["id"]) : true)], false)
    error_message = "EC2 instance resources must have 'id' parameter"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "ecs_service" ? keys(r.params) == tolist(["cluster_name", "desired", "name"]) : true)], false)
    error_message = "ECS Service resources must have 'cluster_name', 'desired' and 'name' parameters"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "fsx_windows_file_system" ? keys(r.params) == tolist(["id", "throughput_capacity"]) : true)], false)
    error_message = "FSx Windows Filesystem resources must have 'id' and 'throughput_capacity' parameters"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "rds_cluster" ? keys(r.params) == tolist(["id"]) : true)], false)
    error_message = "RDS Cluster resources must have 'id' parameter"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "rds_instance" ? keys(r.params) == tolist(["id"]) : true)], false)
    error_message = "RDS Instance resources must have 'id' parameter"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "redshift_cluster" ? keys(r.params) == tolist(["id"]) : true)], false)
    error_message = "Redshift Cluster resources must have 'id' parameter"
  }

  validation {
    condition     = !contains([for r in var.resource_composition : (r.type == "wait" ? keys(r.params) == tolist(["seconds"]) : true)], false)
    error_message = "Wait instructions must have 'seconds' parameter"
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
  description = "Deploy webhooks for external triggers from whitelisted IP CIDR's."
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
