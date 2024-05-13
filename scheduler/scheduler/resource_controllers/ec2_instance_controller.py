import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController

ec2 = boto3.client("ec2")


class Ec2InstanceController(ResourceController):
    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self) -> Tuple[bool, str]:
        ec2.start_instances(InstanceIds=[self.id])
        return (True, f"Instance {self.id} started successfully")

    def stop(self) -> Tuple[bool, str]:
        ec2.stop_instances(InstanceIds=[self.id])
        return (True, f"Instance {self.id} stopped successfully")
