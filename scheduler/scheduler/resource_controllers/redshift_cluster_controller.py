import boto3
from typing import Tuple

from botocore.exceptions import ClientError
from scheduler.resource_controller import ResourceController


class RedshiftClusterController(ResourceController):
    client = boto3.client("redshift")

    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self) -> Tuple[bool, str]:
        try:
            self.client.resume_cluster(ClusterIdentifier=self.id)
            return (True, f"Cluster {self.id} started successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidClusterStateFault":
                return (
                    False,
                    f"Cluster {self.id} is in an invalid state to be started",
                )
            else:
                raise err

    def stop(self) -> Tuple[bool, str]:
        try:
            self.client.pause_cluster(ClusterIdentifier=self.id)
            return (True, f"Cluster {self.id} stopped successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidClusterStateFault":
                return (
                    False,
                    f"Cluster {self.id} is in an invalid state to be stopped",
                )
            else:
                raise err
