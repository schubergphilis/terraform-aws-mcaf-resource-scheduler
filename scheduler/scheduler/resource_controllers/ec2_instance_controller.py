import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController


class Ec2InstanceController(ResourceController):
    client = boto3.client("ec2")

    def __init__(self, id: str):
        super().__init__()
        self.id = id

    def start(self) -> Tuple[bool, str]:
        self.client.start_instances(InstanceIds=[self.id])
        return (True, f"Instance {self.id} started successfully")

    def stop(self) -> Tuple[bool, str]:
        self.client.stop_instances(InstanceIds=[self.id])
        return (True, f"Instance {self.id} stopped successfully")
