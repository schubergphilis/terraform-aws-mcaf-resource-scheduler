import boto3

from botocore.exceptions import ClientError
from scheduler.resource_controller import ResourceController

redshift = boto3.client("redshift")


class RedshiftClusterController(ResourceController):
    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self):
        try:
            redshift.resume_cluster(ClusterIdentifier=self.id)
            self.logger.info(f"Cluster {self.id} started successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidClusterStateFault":
                self.logger.warning(
                    f"Cluster {self.id} is in an invalid state to be started"
                )
            else:
                raise err

    def stop(self):
        try:
            redshift.pause_cluster(ClusterIdentifier=self.id)
            self.logger.info(f"Cluster {self.id} stopped successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidClusterStateFault":
                self.logger.warning(
                    f"Cluster {self.id} is in an invalid state to be stopped"
                )
            else:
                raise err
