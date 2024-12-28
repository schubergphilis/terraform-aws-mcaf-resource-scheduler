from unittest.mock import patch

import botocore.session

from botocore.stub import Stubber

from scheduler.scheduler import handler

ecs = botocore.session.get_session().create_client("ecs")
ecs_stubber = Stubber(ecs)


@patch(
    "scheduler.resource_controllers.ecs_service_controller.EcsServiceController.client",
    ecs,
)
def test_scheduler_ecs_service_start(lambda_context, ecs_service_start):
    with ecs_stubber as stubbed:
        stubbed.add_response(
            "update_service",
            {},
            {"cluster": "ecs-cluster-foo", "desiredCount": 3, "service": "bar-service"},
        )
        response = handler(ecs_service_start, lambda_context)
        assert response == {
            "success": True,
            "message": "Service bar-service started successfully",
        }


@patch(
    "scheduler.resource_controllers.ecs_service_controller.EcsServiceController.client",
    ecs,
)
def test_scheduler_ecs_service_stop(lambda_context, ecs_service_stop):
    with ecs_stubber as stubbed:
        stubbed.add_response(
            "update_service",
            {},
            {"cluster": "ecs-cluster-foo", "desiredCount": 0, "service": "bar-service"},
        )
        response = handler(ecs_service_stop, lambda_context)
        assert response == {
            "success": True,
            "message": "Service bar-service stopped successfully",
        }
