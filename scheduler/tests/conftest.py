from dataclasses import dataclass

import pytest


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = 'test'
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = 'arn:aws:lambda:eu-west-1:809313241:function:test'
        aws_request_id: str = '52fdfc07-2182-154f-163f-5f0f9a621d72'

    return LambdaContext()


@pytest.fixture
def auto_scaling_group_start():
    return {
        'resource_type': 'auto_scaling_group',
        'action': 'start',
        'auto_scaling_group_params': {
            'name': 'asg-test',
            'min': '1',
            'max': '3',
            'desired': '1',
        },
    }


@pytest.fixture
def auto_scaling_group_stop():
    return {
        'resource_type': 'auto_scaling_group',
        'action': 'stop',
        'auto_scaling_group_params': {
            'name': 'asg-test',
            'min': '1',
            'max': '3',
            'desired': '1',
        },
    }


@pytest.fixture
def ec2_instance_start():
    return {
        'resource_type': 'ec2_instance',
        'action': 'start',
        'ec2_instance_params': {'id': 'i-4abc123'},
    }


@pytest.fixture
def ec2_instance_stop():
    return {
        'resource_type': 'ec2_instance',
        'action': 'stop',
        'ec2_instance_params': {'id': 'i-4abc123'},
    }


@pytest.fixture
def ecs_service_start():
    return {
        'resource_type': 'ecs_service',
        'action': 'start',
        'ecs_service_params': {
            'cluster_name': 'ecs-cluster-foo',
            'name': 'bar-service',
            'desired': '3',
        },
    }


@pytest.fixture
def ecs_service_stop():
    return {
        'resource_type': 'ecs_service',
        'action': 'stop',
        'ecs_service_params': {
            'cluster_name': 'ecs-cluster-foo',
            'name': 'bar-service',
            'desired': '3',
        },
    }


@pytest.fixture
def efs_file_system_start():
    return {
        'resource_type': 'efs_file_system',
        'action': 'start',
        'efs_file_system_params': {
            'id': 'fs-1234567890',
            'provisioned_throughput_in_mibps': '128',
        },
    }


@pytest.fixture
def efs_file_system_stop():
    return {
        'resource_type': 'efs_file_system',
        'action': 'stop',
        'efs_file_system_params': {
            'id': 'fs-1234567890',
            'provisioned_throughput_in_mibps': '128',
        },
    }


@pytest.fixture
def fsx_windows_file_system_start():
    return {
        'resource_type': 'fsx_windows_file_system',
        'action': 'start',
        'fsx_windows_file_system_params': {
            'id': 'fs-1234567890',
            'throughput_capacity': '512',
        },
    }


@pytest.fixture
def fsx_windows_file_system_stop():
    return {
        'resource_type': 'fsx_windows_file_system',
        'action': 'stop',
        'fsx_windows_file_system_params': {
            'id': 'fs-1234567890',
            'throughput_capacity': '512',
        },
    }


@pytest.fixture
def rds_cluster_start():
    return {
        'resource_type': 'rds_cluster',
        'action': 'start',
        'rds_cluster_params': {'id': 'rds-cluster-test'},
    }


@pytest.fixture
def rds_cluster_stop():
    return {
        'resource_type': 'rds_cluster',
        'action': 'stop',
        'rds_cluster_params': {'id': 'rds-cluster-test'},
    }


@pytest.fixture
def rds_instance_start():
    return {
        'resource_type': 'rds_instance',
        'action': 'start',
        'rds_instance_params': {'id': 'rds-instance-test'},
    }


@pytest.fixture
def rds_instance_stop():
    return {
        'resource_type': 'rds_instance',
        'action': 'stop',
        'rds_instance_params': {'id': 'rds-instance-test'},
    }


@pytest.fixture
def redshift_cluster_start():
    return {
        'resource_type': 'redshift_cluster',
        'action': 'start',
        'redshift_cluster_params': {'id': 'redshift-cluster-test'},
    }


@pytest.fixture
def redshift_cluster_stop():
    return {
        'resource_type': 'redshift_cluster',
        'action': 'stop',
        'redshift_cluster_params': {'id': 'redshift-cluster-test'},
    }
