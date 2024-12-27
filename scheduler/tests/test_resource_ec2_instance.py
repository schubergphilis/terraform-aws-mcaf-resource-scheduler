from unittest.mock import patch

import botocore.session

from botocore.stub import Stubber

from scheduler.scheduler import handler

ec2 = botocore.session.get_session().create_client("ec2")
ec2_stubber = Stubber(ec2)


@patch(
    "scheduler.resource_controllers.ec2_instance_controller.Ec2InstanceController.client",
    ec2,
)
def test_scheduler_ec2_instance_start(lambda_context):
    payload = {
        "resource_type": "ec2_instance",
        "action": "start",
        "ec2_instance_params": {"id": "i-4abc123"},
    }

    with ec2_stubber as stubbed:
        stubbed.add_response(
            "start_instances",
            {},
            {"InstanceIds": ["i-4abc123"]},
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Instance i-4abc123 started successfully",
        }


@patch(
    "scheduler.resource_controllers.ec2_instance_controller.Ec2InstanceController.client",
    ec2,
)
def test_scheduler_ec2_instance_stop(lambda_context):
    payload = {
        "resource_type": "ec2_instance",
        "action": "stop",
        "ec2_instance_params": {"id": "i-4abc123"},
    }

    with ec2_stubber as stubbed:
        stubbed.add_response(
            "stop_instances",
            {},
            {"InstanceIds": ["i-4abc123"]},
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Instance i-4abc123 stopped successfully",
        }
