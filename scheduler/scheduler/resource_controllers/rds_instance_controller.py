import boto3
from typing import Tuple

from botocore.exceptions import ClientError
from scheduler.resource_controller import ResourceController


class RdsInstanceController(ResourceController):
    client = boto3.client('rds')

    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self) -> Tuple[bool, str]:
        try:
            self.client.start_db_instance(DBInstanceIdentifier=self.id)
            return (True, f'Instance {self.id} started successfully')
        except ClientError as err:
            if err.response['Error']['Code'] == 'InvalidDBInstanceStateFault':
                return (
                    False,
                    f'Instance {self.id} is in an invalid state to be started',
                )
            else:
                raise err

    def stop(self) -> Tuple[bool, str]:
        try:
            self.client.stop_db_instance(DBInstanceIdentifier=self.id)
            return (True, f'Instance {self.id} stopped successfully')
        except ClientError as err:
            if err.response['Error']['Code'] == 'InvalidDBInstanceStateFault':
                return (
                    False,
                    f'Instance {self.id} is in an invalid state to be stopped',
                )
            else:
                raise err
