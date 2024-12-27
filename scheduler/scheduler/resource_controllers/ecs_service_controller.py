import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController


class EcsServiceController(ResourceController):
    client = boto3.client("ecs")

    def __init__(self, cluster_name: str, name: str, desired: str):
        super().__init__()
        self.cluster_name = cluster_name
        self.name = name
        self.desired = int(desired)

    def start(self) -> Tuple[bool, str]:
        self.client.update_service(
            cluster=self.cluster_name, service=self.name, desiredCount=self.desired
        )
        return (True, f"Service {self.name} started successfully")

    def stop(self) -> Tuple[bool, str]:
        self.client.update_service(
            cluster=self.cluster_name, service=self.name, desiredCount=0
        )
        return (True, f"Service {self.name} stopped successfully")
