import pytest

from unittest.mock import patch

import botocore.session

from botocore.exceptions import ClientError
from botocore.stub import Stubber

from scheduler.scheduler import handler

rds = botocore.session.get_session().create_client("rds")
rds_stubber = Stubber(rds)


@patch(
    "scheduler.resource_controllers.rds_cluster_controller.RdsClusterController.client",
    rds,
)
def test_scheduler_rds_cluster_start(lambda_context):
    payload = {
        "resource_type": "rds_cluster",
        "action": "start",
        "rds_cluster_params": {"id": "rds-cluster-test"},
    }

    with rds_stubber as stubbed:
        stubbed.add_response(
            "start_db_cluster",
            {},
            {"DBClusterIdentifier": "rds-cluster-test"},
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Cluster rds-cluster-test started successfully",
        }


@patch(
    "scheduler.resource_controllers.rds_cluster_controller.RdsClusterController.client",
    rds,
)
def test_scheduler_rds_cluster_stop(lambda_context):
    payload = {
        "resource_type": "rds_cluster",
        "action": "stop",
        "rds_cluster_params": {"id": "rds-cluster-test"},
    }

    with rds_stubber as stubbed:
        stubbed.add_response(
            "stop_db_cluster",
            {},
            {"DBClusterIdentifier": "rds-cluster-test"},
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": True,
            "message": "Cluster rds-cluster-test stopped successfully",
        }


@patch(
    "scheduler.resource_controllers.rds_cluster_controller.RdsClusterController.client",
    rds,
)
def test_scheduler_skips_rds_cluster_start_on_invalid_cluster_state(lambda_context):
    payload = {
        "resource_type": "rds_cluster",
        "action": "start",
        "rds_cluster_params": {"id": "rds-cluster-test"},
    }

    with rds_stubber as stubbed:
        stubbed.add_client_error(
            "start_db_cluster", service_error_code="InvalidDBClusterStateFault"
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": False,
            "message": "Cluster rds-cluster-test is in an invalid state to be started",
        }


@patch(
    "scheduler.resource_controllers.rds_cluster_controller.RdsClusterController.client",
    rds,
)
def test_scheduler_skips_rds_cluster_stop_on_invalid_cluster_state(lambda_context):
    payload = {
        "resource_type": "rds_cluster",
        "action": "stop",
        "rds_cluster_params": {"id": "rds-cluster-test"},
    }

    with rds_stubber as stubbed:
        stubbed.add_client_error(
            "stop_db_cluster", service_error_code="InvalidDBClusterStateFault"
        )
        response = handler(payload, lambda_context)
        assert response == {
            "success": False,
            "message": "Cluster rds-cluster-test is in an invalid state to be stopped",
        }


@patch(
    "scheduler.resource_controllers.rds_cluster_controller.RdsClusterController.client",
    rds,
)
def test_scheduler_rds_cluster_start_on_non_existing_cluster_raises_error(
    lambda_context,
):
    payload = {
        "resource_type": "rds_cluster",
        "action": "start",
        "rds_cluster_params": {"id": "rds-cluster-test"},
    }

    with pytest.raises(ClientError):
        with rds_stubber as stubbed:
            stubbed.add_client_error(
                "start_db_cluster", service_error_code="DBClusterNotFoundFault"
            )
            handler(payload, lambda_context)


@patch(
    "scheduler.resource_controllers.rds_cluster_controller.RdsClusterController.client",
    rds,
)
def test_scheduler_rds_cluster_stop_on_non_existing_cluster_raises_error(
    lambda_context,
):
    payload = {
        "resource_type": "rds_cluster",
        "action": "stop",
        "rds_cluster_params": {"id": "rds-cluster-test"},
    }

    with pytest.raises(ClientError):
        with rds_stubber as stubbed:
            stubbed.add_client_error(
                "stop_db_cluster", service_error_code="DBClusterNotFoundFault"
            )
            handler(payload, lambda_context)
