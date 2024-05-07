import boto3

from botocore.exceptions import ClientError
from scheduler.resource_controller import ResourceController

rds = boto3.client("rds")


class RdsInstanceController(ResourceController):
    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self):
        try:
            rds.start_db_instance(DBInstanceIdentifier=self.id)
            self.logger.info(f"Instance {self.id} started successfully")
        except ClientError as err:
            if err.response["Error"]["Code"] == "InvalidDBInstanceState":
                self.logger.warning(
                    f"Instance {self.id} is in an invalid state to be started"
                )
            else:
                raise err

    def stop(self):
        try:
            rds.stop_db_instance(DBInstanceIdentifier=self.id)
            self.logger.info(f"Instance {self.id} stopped successfully")
        except ClientError as err:
            print(err.response)
            if err.response["Error"]["Code"] == "InvalidDBInstanceState":
                self.logger.warning(
                    f"Instance {self.id} is in an invalid state to be stopped"
                )
            else:
                raise err
