import boto3
from typing import Tuple

from botocore.exceptions import ClientError
from scheduler.resource_controller import ResourceController

rds = boto3.client("rds")


class RdsClusterController(ResourceController):
    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self) -> Tuple[bool, str]:
        try:
            rds.start_db_cluster(DBClusterIdentifier=self.id)
            return (True, f"Cluster {self.id} started successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidDBInstanceState":
                return (
                    False,
                    f"Cluster {self.id} is in an invalid state to be started",
                )
            else:
                raise err

    def stop(self) -> Tuple[bool, str]:
        try:
            rds.stop_db_cluster(DBClusterIdentifier=self.id)
            return (True, f"Cluster {self.id} stopped successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidDBInstanceState":
                return (
                    False,
                    f"Cluster {self.id} is in an invalid state to be stopped",
                )
            else:
                raise err
