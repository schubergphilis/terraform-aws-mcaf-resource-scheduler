INPUT = {
    "$schema": "https://json-schema.org/draft-07/schema",
    "type": "object",
    "title": "Resource Scheduler Schema",
    "properties": {
        "action": {
            "type": "string",
            "title": "The action to perform",
            "enum": ["start", "stop", "extend_windows"],
        },
        "resource_type": {
            "type": "string",
            "enum": [
                "auto_scaling_group",
                "cron_helper",
                "ec2_instance",
                "ecs_service",
                "fsx_windows_file_system",
                "rds_cluster",
                "rds_instance",
                "redshift_cluster",
            ],
        },
        "cron_helper_params": {
            "type": "object",
            "properties": {
                "aws_window_expression": {"type": "string"},
                "minutes": {"type": "number"},
                "start_resources_at": {"type": "string"},
                "stop_resources_at": {"type": "string"},
                "timezone": {"type": "string"},
            },
            "required": ["aws_window_expression", "minutes"],
        },
        "rds_instance_params": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
        "rds_cluster_params": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
        "redshift_cluster_params": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
        "ec2_instance_params": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
        "auto_scaling_group_params": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "min": {"type": "string"},
                "max": {"type": "string"},
                "desired": {"type": "string"},
            },
            "required": ["name", "min", "max", "desired"],
        },
        "ecs_service_params": {
            "type": "object",
            "properties": {
                "cluster_name": {
                    "type": "string",
                },
                "name": {"type": "string"},
                "desired": {"type": "string"},
            },
            "required": ["cluster_name", "name", "desired"],
        },
        "fsx_windows_file_system_params": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                },
                "start_throughput_capacity": {"type": "string"},
                "stop_throughput_capacity": {"type": "string"},
            },
            "required": [
                "id",
                "start_throughput_capacity",
                "stop_throughput_capacity",
            ],
        },
    },
    "allOf": [
        {"required": ["action", "resource_type"]},
        {
            "if": {"properties": {"resource_type": {"const": "rds_instance"}}},
            "then": {"required": ["rds_instance_params"]},
        },
        {
            "if": {"properties": {"resource_type": {"const": "cron_helper"}}},
            "then": {"required": ["cron_helper_params"]},
        },
        {
            "if": {"properties": {"resource_type": {"const": "rds_cluster"}}},
            "then": {"required": ["rds_cluster_params"]},
        },
        {
            "if": {"properties": {"resource_type": {"const": "redshift_cluster"}}},
            "then": {"required": ["redshift_cluster_params"]},
        },
        {
            "if": {"properties": {"resource_type": {"const": "auto_scaling_group"}}},
            "then": {"required": ["auto_scaling_group_params"]},
        },
        {
            "if": {"properties": {"resource_type": {"const": "ecs_service"}}},
            "then": {"required": ["ecs_service_params"]},
        },
        {
            "if": {"properties": {"resource_type": {"const": "ec2_instance"}}},
            "then": {"required": ["ec2_instance_params"]},
        },
    ],
}

OUTPUT = {}
