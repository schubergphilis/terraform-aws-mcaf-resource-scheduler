from unittest.mock import patch

import botocore.session

from botocore.stub import Stubber

from scheduler.scheduler import handler

autoscaling = botocore.session.get_session().create_client('autoscaling')
autoscaling_stubber = Stubber(autoscaling)


@patch(
    'scheduler.resource_controllers.auto_scaling_group_controller.AutoScalingGroupController.client',
    autoscaling,
)
def test_scheduler_auto_scaling_group_start(lambda_context, auto_scaling_group_start):
    with autoscaling_stubber as stubbed:
        stubbed.add_response(
            'update_auto_scaling_group',
            {},
            {
                'AutoScalingGroupName': 'asg-test',
                'MinSize': 1,
                'MaxSize': 3,
                'DesiredCapacity': 1,
            },
        )
        response = handler(auto_scaling_group_start, lambda_context)
        assert response == {
            'success': True,
            'message': 'Auto-Scaling Group asg-test started successfully',
        }


@patch(
    'scheduler.resource_controllers.auto_scaling_group_controller.AutoScalingGroupController.client',
    autoscaling,
)
def test_scheduler_auto_scaling_group_stop(lambda_context, auto_scaling_group_stop):
    with autoscaling_stubber as stubbed:
        stubbed.add_response(
            'update_auto_scaling_group',
            {},
            {
                'AutoScalingGroupName': 'asg-test',
                'MinSize': 0,
                'MaxSize': 0,
                'DesiredCapacity': 0,
            },
        )
        response = handler(auto_scaling_group_stop, lambda_context)
        assert response == {
            'success': True,
            'message': 'Auto-Scaling Group asg-test stopped successfully',
        }
