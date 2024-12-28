import pytest

from unittest.mock import patch

import botocore.session

from botocore.exceptions import ClientError
from botocore.stub import Stubber

from scheduler.scheduler import handler

rds = botocore.session.get_session().create_client("rds")
rds_stubber = Stubber(rds)


@patch(
    "scheduler.resource_controllers.rds_instance_controller.RdsInstanceController.client",
    rds,
)
def test_scheduler_rds_instance_start(lambda_context, rds_instance_start):
    with rds_stubber as stubbed:
        stubbed.add_response(
            "start_db_instance",
            {},
            {"DBInstanceIdentifier": "rds-instance-test"},
        )
        response = handler(rds_instance_start, lambda_context)
        assert response == {
            "success": True,
            "message": "Instance rds-instance-test started successfully",
        }


@patch(
    "scheduler.resource_controllers.rds_instance_controller.RdsInstanceController.client",
    rds,
)
def test_scheduler_rds_instance_stop(lambda_context, rds_instance_stop):
    with rds_stubber as stubbed:
        stubbed.add_response(
            "stop_db_instance",
            {},
            {"DBInstanceIdentifier": "rds-instance-test"},
        )
        response = handler(rds_instance_stop, lambda_context)
        assert response == {
            "success": True,
            "message": "Instance rds-instance-test stopped successfully",
        }


@patch(
    "scheduler.resource_controllers.rds_instance_controller.RdsInstanceController.client",
    rds,
)
def test_scheduler_skips_rds_instance_start_on_invalid_instance_state(
    lambda_context, rds_instance_start
):
    with rds_stubber as stubbed:
        stubbed.add_client_error(
            "start_db_instance", service_error_code="InvalidDBInstanceStateFault"
        )
        response = handler(rds_instance_start, lambda_context)
        assert response == {
            "success": False,
            "message": "Instance rds-instance-test is in an invalid state to be started",
        }


@patch(
    "scheduler.resource_controllers.rds_instance_controller.RdsInstanceController.client",
    rds,
)
def test_scheduler_skips_rds_instance_stop_on_invalid_instance_state(
    lambda_context, rds_instance_stop
):
    with rds_stubber as stubbed:
        stubbed.add_client_error(
            "stop_db_instance", service_error_code="InvalidDBInstanceStateFault"
        )
        response = handler(rds_instance_stop, lambda_context)
        assert response == {
            "success": False,
            "message": "Instance rds-instance-test is in an invalid state to be stopped",
        }


@patch(
    "scheduler.resource_controllers.rds_instance_controller.RdsInstanceController.client",
    rds,
)
def test_scheduler_rds_instance_start_on_non_existing_instance_raises_error(
    lambda_context, rds_instance_start
):
    with pytest.raises(ClientError):
        with rds_stubber as stubbed:
            stubbed.add_client_error(
                "start_db_instance", service_error_code="DBInstanceNotFoundFault"
            )
            handler(rds_instance_start, lambda_context)


@patch(
    "scheduler.resource_controllers.rds_instance_controller.RdsInstanceController.client",
    rds,
)
def test_scheduler_rds_instance_stop_on_non_existing_instance_raises_error(
    lambda_context, rds_instance_stop
):
    with pytest.raises(ClientError):
        with rds_stubber as stubbed:
            stubbed.add_client_error(
                "stop_db_instance", service_error_code="DBInstanceNotFoundFault"
            )
            handler(rds_instance_stop, lambda_context)
