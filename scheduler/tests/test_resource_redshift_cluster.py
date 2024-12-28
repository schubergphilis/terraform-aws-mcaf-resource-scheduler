import pytest

from unittest.mock import patch

import botocore.session

from botocore.exceptions import ClientError
from botocore.stub import Stubber

from scheduler.scheduler import handler

redshift = botocore.session.get_session().create_client("redshift")
redshift_stubber = Stubber(redshift)


@patch(
    "scheduler.resource_controllers.redshift_cluster_controller.RedshiftClusterController.client",
    redshift,
)
def test_scheduler_redshift_cluster_start(lambda_context, redshift_cluster_start):
    with redshift_stubber as stubbed:
        stubbed.add_response(
            "resume_cluster",
            {},
            {"ClusterIdentifier": "redshift-cluster-test"},
        )
        response = handler(redshift_cluster_start, lambda_context)
        assert response == {
            "success": True,
            "message": "Cluster redshift-cluster-test started successfully",
        }


@patch(
    "scheduler.resource_controllers.redshift_cluster_controller.RedshiftClusterController.client",
    redshift,
)
def test_scheduler_redshift_cluster_stop(lambda_context, redshift_cluster_stop):
    with redshift_stubber as stubbed:
        stubbed.add_response(
            "pause_cluster",
            {},
            {"ClusterIdentifier": "redshift-cluster-test"},
        )
        response = handler(redshift_cluster_stop, lambda_context)
        assert response == {
            "success": True,
            "message": "Cluster redshift-cluster-test stopped successfully",
        }


@patch(
    "scheduler.resource_controllers.redshift_cluster_controller.RedshiftClusterController.client",
    redshift,
)
def test_scheduler_skips_redshift_cluster_start_on_invalid_cluster_state(
    lambda_context, redshift_cluster_start
):
    with redshift_stubber as stubbed:
        stubbed.add_client_error(
            "resume_cluster", service_error_code="InvalidClusterStateFault"
        )
        response = handler(redshift_cluster_start, lambda_context)
        assert response == {
            "success": False,
            "message": "Cluster redshift-cluster-test is in an invalid state to be started",
        }


@patch(
    "scheduler.resource_controllers.redshift_cluster_controller.RedshiftClusterController.client",
    redshift,
)
def test_scheduler_skips_redshift_cluster_stop_on_invalid_cluster_state(
    lambda_context, redshift_cluster_stop
):
    with redshift_stubber as stubbed:
        stubbed.add_client_error(
            "pause_cluster", service_error_code="InvalidClusterStateFault"
        )
        response = handler(redshift_cluster_stop, lambda_context)
        assert response == {
            "success": False,
            "message": "Cluster redshift-cluster-test is in an invalid state to be stopped",
        }


@patch(
    "scheduler.resource_controllers.redshift_cluster_controller.RedshiftClusterController.client",
    redshift,
)
def test_scheduler_redshift_cluster_start_on_non_existing_cluster_raises_error(
    lambda_context, redshift_cluster_start
):
    with pytest.raises(ClientError):
        with redshift_stubber as stubbed:
            stubbed.add_client_error(
                "resume_cluster", service_error_code="ClusterNotFoundFault"
            )
            handler(redshift_cluster_start, lambda_context)


@patch(
    "scheduler.resource_controllers.redshift_cluster_controller.RedshiftClusterController.client",
    redshift,
)
def test_scheduler_redshift_cluster_stop_on_non_existing_cluster_raises_error(
    lambda_context, redshift_cluster_stop
):
    with pytest.raises(ClientError):
        with redshift_stubber as stubbed:
            stubbed.add_client_error(
                "pause_cluster", service_error_code="ClusterNotFoundFault"
            )
            handler(redshift_cluster_stop, lambda_context)
