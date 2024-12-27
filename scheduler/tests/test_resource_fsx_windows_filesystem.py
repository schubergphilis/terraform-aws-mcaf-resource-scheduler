from unittest.mock import patch

import botocore.session

from botocore.stub import Stubber

from scheduler.scheduler import handler

fsx = botocore.session.get_session().create_client("fsx")
fsx_stubber = Stubber(fsx)


@patch(
    "scheduler.resource_controllers.fsx_windows_file_system_controller.FsxWindowsFileSystemController.client",
    fsx,
)
def test_scheduler_fsx_windows_file_system_start(lambda_context):
    payload = {
        "resource_type": "fsx_windows_file_system",
        "action": "start",
        "fsx_windows_file_system_params": {
            "id": "fs-1234567890",
            "throughput_capacity": "512",
        },
    }

    with fsx_stubber as stubbed:
        stubbed.add_response(
            "update_file_system",
            {},
            {
                "FileSystemId": "fs-1234567890",
                "WindowsConfiguration": {"ThroughputCapacity": 512},
            },
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Throughput capacity for fs-1234567890 started adjustment to 512 MB/s",
        }


@patch(
    "scheduler.resource_controllers.fsx_windows_file_system_controller.FsxWindowsFileSystemController.client",
    fsx,
)
def test_scheduler_fsx_windows_file_system_stop(lambda_context):
    payload = {
        "resource_type": "fsx_windows_file_system",
        "action": "stop",
        "fsx_windows_file_system_params": {
            "id": "fs-1234567890",
            "throughput_capacity": "512",
        },
    }

    with fsx_stubber as stubbed:
        stubbed.add_response(
            "update_file_system",
            {},
            {
                "FileSystemId": "fs-1234567890",
                "WindowsConfiguration": {"ThroughputCapacity": 32},
            },
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Throughput capacity for fs-1234567890 started adjustment to 32 MB/s",
        }
