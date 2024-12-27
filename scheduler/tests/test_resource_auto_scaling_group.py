from unittest.mock import patch

import botocore.session

from botocore.stub import Stubber

from scheduler.scheduler import handler

autoscaling = botocore.session.get_session().create_client("autoscaling")
autoscaling_stubber = Stubber(autoscaling)


@patch(
    "scheduler.resource_controllers.auto_scaling_group_controller.AutoScalingGroupController.client",
    autoscaling,
)
def test_scheduler_auto_scaling_group_start(lambda_context):
    payload = {
        "resource_type": "auto_scaling_group",
        "action": "start",
        "auto_scaling_group_params": {
            "name": "asg-test",
            "min": "1",
            "max": "3",
            "desired": "1",
        },
    }

    with autoscaling_stubber as stubbed:
        stubbed.add_response(
            "update_auto_scaling_group",
            {},
            {
                "AutoScalingGroupName": "asg-test",
                "MinSize": 1,
                "MaxSize": 3,
                "DesiredCapacity": 1,
            },
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Auto-Scaling Group asg-test started successfully",
        }


@patch(
    "scheduler.resource_controllers.auto_scaling_group_controller.AutoScalingGroupController.client",
    autoscaling,
)
def test_scheduler_auto_scaling_group_stop(lambda_context):
    payload = {
        "resource_type": "auto_scaling_group",
        "action": "stop",
        "auto_scaling_group_params": {
            "name": "asg-test",
            "min": "1",
            "max": "3",
            "desired": "1",
        },
    }

    with autoscaling_stubber as stubbed:
        stubbed.add_response(
            "update_auto_scaling_group",
            {},
            {
                "AutoScalingGroupName": "asg-test",
                "MinSize": 0,
                "MaxSize": 0,
                "DesiredCapacity": 0,
            },
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Auto-Scaling Group asg-test stopped successfully",
        }
