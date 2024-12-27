from unittest.mock import patch

import botocore.session

from botocore.stub import Stubber

from scheduler.scheduler import handler

efs = botocore.session.get_session().create_client("efs")
efs_stubber = Stubber(efs)


@patch(
    "scheduler.resource_controllers.efs_file_system_controller.EfsFileSystemController.client",
    efs,
)
def test_scheduler_efs_file_system_start(lambda_context):
    payload = {
        "resource_type": "efs_file_system",
        "action": "start",
        "efs_file_system_params": {
            "id": "fs-1234567890",
            "provisioned_throughput_in_mibps": "128",
        },
    }

    with efs_stubber as stubbed:
        stubbed.add_response(
            "describe_file_systems",
            {
                "FileSystems": [
                    {
                        "FileSystemId": "fs-1234567890",
                        "ThroughputMode": "provisioned",
                        "OwnerId": "1234567890",
                        "CreationToken": "foo",
                        "CreationTime": "2021-01-01T00:00:00Z",
                        "LifeCycleState": "available",
                        "NumberOfMountTargets": 1,
                        "SizeInBytes": {
                            "Value": 0,
                            "ValueInIA": 0,
                            "ValueInStandard": 0,
                        },
                        "PerformanceMode": "generalPurpose",
                        "Tags": [{"Key": "Name", "Value": "bar"}],
                    }
                ]
            },
            {"FileSystemId": "fs-1234567890"},
        )
        stubbed.add_response(
            "update_file_system",
            {
                "FileSystemId": "fs-1234567890",
                "ThroughputMode": "provisioned",
                "OwnerId": "1234567890",
                "CreationToken": "foo",
                "CreationTime": "2021-01-01T00:00:00Z",
                "LifeCycleState": "available",
                "NumberOfMountTargets": 1,
                "SizeInBytes": {"Value": 0, "ValueInIA": 0, "ValueInStandard": 0},
                "PerformanceMode": "generalPurpose",
                "Tags": [{"Key": "Name", "Value": "bar"}],
            },
            {
                "FileSystemId": "fs-1234567890",
                "ThroughputMode": "provisioned",
                "ProvisionedThroughputInMibps": 128.0,
            },
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Throughput capacity for fs-1234567890 adjusted to 128.0 MB/s",
        }


@patch(
    "scheduler.resource_controllers.efs_file_system_controller.EfsFileSystemController.client",
    efs,
)
def test_scheduler_efs_file_system_stop(lambda_context):
    payload = {
        "resource_type": "efs_file_system",
        "action": "stop",
        "efs_file_system_params": {
            "id": "fs-1234567890",
            "provisioned_throughput_in_mibps": "128",
        },
    }

    with efs_stubber as stubbed:
        stubbed.add_response(
            "describe_file_systems",
            {
                "FileSystems": [
                    {
                        "FileSystemId": "fs-1234567890",
                        "ThroughputMode": "provisioned",
                        "OwnerId": "1234567890",
                        "CreationToken": "foo",
                        "CreationTime": "2021-01-01T00:00:00Z",
                        "LifeCycleState": "available",
                        "NumberOfMountTargets": 1,
                        "SizeInBytes": {
                            "Value": 0,
                            "ValueInIA": 0,
                            "ValueInStandard": 0,
                        },
                        "PerformanceMode": "generalPurpose",
                        "Tags": [{"Key": "Name", "Value": "bar"}],
                    }
                ]
            },
            {"FileSystemId": "fs-1234567890"},
        )
        stubbed.add_response(
            "update_file_system",
            {
                "FileSystemId": "fs-1234567890",
                "ThroughputMode": "provisioned",
                "OwnerId": "1234567890",
                "CreationToken": "foo",
                "CreationTime": "2021-01-01T00:00:00Z",
                "LifeCycleState": "available",
                "NumberOfMountTargets": 1,
                "SizeInBytes": {"Value": 0, "ValueInIA": 0, "ValueInStandard": 0},
                "PerformanceMode": "generalPurpose",
                "Tags": [{"Key": "Name", "Value": "bar"}],
            },
            {
                "FileSystemId": "fs-1234567890",
                "ThroughputMode": "provisioned",
                "ProvisionedThroughputInMibps": 1.0,
            },
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Throughput capacity for fs-1234567890 adjusted to 1.0 MB/s",
        }


@patch(
    "scheduler.resource_controllers.efs_file_system_controller.EfsFileSystemController.client",
    efs,
)
def test_scheduler_skips_efs_file_system_start_if_no_provisioned_throughput_mode(
    lambda_context,
):
    payload = {
        "resource_type": "efs_file_system",
        "action": "start",
        "efs_file_system_params": {
            "id": "fs-1234567890",
            "provisioned_throughput_in_mibps": "128",
        },
    }

    with efs_stubber as stubbed:
        stubbed.add_response(
            "describe_file_systems",
            {
                "FileSystems": [
                    {
                        "FileSystemId": "fs-1234567890",
                        "ThroughputMode": "elastic",
                        "OwnerId": "1234567890",
                        "CreationToken": "foo",
                        "CreationTime": "2021-01-01T00:00:00Z",
                        "LifeCycleState": "available",
                        "NumberOfMountTargets": 1,
                        "SizeInBytes": {
                            "Value": 0,
                            "ValueInIA": 0,
                            "ValueInStandard": 0,
                        },
                        "PerformanceMode": "generalPurpose",
                        "Tags": [{"Key": "Name", "Value": "bar"}],
                    }
                ]
            },
            {"FileSystemId": "fs-1234567890"},
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": False,
            "message": "EFS Filesystem fs-1234567890 is not in provisioned throughput mode",
        }


@patch(
    "scheduler.resource_controllers.efs_file_system_controller.EfsFileSystemController.client",
    efs,
)
def test_scheduler_skips_efs_file_system_stop_if_no_provisioned_throughput_mode(
    lambda_context,
):
    payload = {
        "resource_type": "efs_file_system",
        "action": "stop",
        "efs_file_system_params": {
            "id": "fs-1234567890",
            "provisioned_throughput_in_mibps": "128",
        },
    }

    with efs_stubber as stubbed:
        stubbed.add_response(
            "describe_file_systems",
            {
                "FileSystems": [
                    {
                        "FileSystemId": "fs-1234567890",
                        "ThroughputMode": "elastic",
                        "OwnerId": "1234567890",
                        "CreationToken": "foo",
                        "CreationTime": "2021-01-01T00:00:00Z",
                        "LifeCycleState": "available",
                        "NumberOfMountTargets": 1,
                        "SizeInBytes": {
                            "Value": 0,
                            "ValueInIA": 0,
                            "ValueInStandard": 0,
                        },
                        "PerformanceMode": "generalPurpose",
                        "Tags": [{"Key": "Name", "Value": "bar"}],
                    }
                ]
            },
            {"FileSystemId": "fs-1234567890"},
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": False,
            "message": "EFS Filesystem fs-1234567890 is not in provisioned throughput mode",
        }
