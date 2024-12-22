import pytest

from botocore.exceptions import NoCredentialsError

from scheduler.scheduler import handler


def test_scheduler_cron_helper_extend_windows(lambda_context):
    payload = {
        "resource_type": "cron_helper",
        "action": "extend_windows",
        "cron_helper_params": {
            "aws_window_expression" :"Thu:00:00-Thu:02:00",
            "minutes": 15,
            "start_resources_at": "0 9 ? * * *",
            "stop_resources_at": "0 18 ? * * *",
            "timezone": "Europe/Amsterdam"
        }
    }

    out = handler(payload, lambda_context)
    assert out == {
        "start": "45 23 ? * WED *",
        "stop": "15 2 ? * THU *",
        "skip_start": False,
        "skip_stop": False
    }

def test_scheduler_ecs_service_start(lambda_context):
    payload = {
        "resource_type": "ecs_service",
        "action": "start",
        "ecs_service_params": {
            "cluster_name" :"ecs-cluster-foo",
            "name": "bar-service",
            "desired": "3"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_ecs_service_stop(lambda_context):
    payload = {
        "resource_type": "ecs_service",
        "action": "stop",
        "ecs_service_params": {
            "cluster_name" :"ecs-cluster-foo",
            "name": "bar-service",
            "desired": "3"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_ec2_instance_start(lambda_context):
    payload = {
        "resource_type": "ec2_instance",
        "action": "start",
        "ec2_instance_params": {
            "id" :"i-4abc123"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_ec2_instance_stop(lambda_context):
    payload = {
        "resource_type": "ec2_instance",
        "action": "stop",
        "ec2_instance_params": {
            "id" :"i-4abc123"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_auto_scaling_group_start(lambda_context):
    payload = {
        "resource_type": "auto_scaling_group",
        "action": "start",
        "auto_scaling_group_params": {
            "name": "asg-test",
            "min": "1",
            "max": "3",
            "desired": "1",
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_auto_scaling_group_stop(lambda_context):
    payload = {
        "resource_type": "auto_scaling_group",
        "action": "stop",
        "auto_scaling_group_params": {
            "name": "asg-test",
            "min": "1",
            "max": "3",
            "desired": "1",
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_rds_cluster_start(lambda_context):
    payload = {
        "resource_type": "rds_cluster",
        "action": "start",
        "rds_cluster_params": {
            "id": "rds-cluster-test"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_rds_cluster_stop(lambda_context):
    payload = {
        "resource_type": "rds_cluster",
        "action": "stop",
        "rds_cluster_params": {
            "id": "rds-cluster-test"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_rds_instance_start(lambda_context):
    payload = {
        "resource_type": "rds_instance",
        "action": "start",
        "rds_instance_params": {
            "id": "rds-instance-test"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_rds_instance_stop(lambda_context):
    payload = {
        "resource_type": "rds_instance",
        "action": "stop",
        "rds_instance_params": {
            "id": "rds-instance-test"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_redshift_cluster_start(lambda_context):
    payload = {
        "resource_type": "redshift_cluster",
        "action": "start",
        "redshift_cluster_params": {
            "id": "redshift-cluster-test"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_redshift_cluster_stop(lambda_context):
    payload = {
        "resource_type": "redshift_cluster",
        "action": "stop",
        "redshift_cluster_params": {
            "id": "redshift-cluster-test"
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_fsx_windows_file_system_start(lambda_context):
    payload = {
        "resource_type": "fsx_windows_file_system",
        "action": "start",
        "fsx_windows_file_system_params": {
            "id": "fs-1234567890",
            "throughput_capacity": "512",
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_fsx_windows_file_system_stop(lambda_context):
    payload = {
        "resource_type": "fsx_windows_file_system",
        "action": "stop",
        "fsx_windows_file_system_params": {
            "id": "fs-1234567890",
            "throughput_capacity": "512",
        }
    }

def test_scheduler_efs_file_system_start(lambda_context):
    payload = {
        "resource_type": "efs_file_system",
        "action": "start",
        "efs_file_system_params": {
            "id": "fs-1234567890",
            "provisioned_throughput_in_mibps": "128",
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)

def test_scheduler_efs_file_system_stop(lambda_context):
    payload = {
        "resource_type": "efs_file_system",
        "action": "stop",
        "efs_file_system_params": {
            "id": "fs-1234567890",
            "provisioned_throughput_in_mibps": "128",
        }
    }

    with pytest.raises(NoCredentialsError):
        handler(payload, lambda_context)
