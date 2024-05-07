import boto3

from scheduler.resource_controller import ResourceController

ecs = boto3.client("ecs")


class EcsServiceController(ResourceController):
    def __init__(self, cluster_name: str, name: str, desired: str):
        super().__init__()
        self.cluster_name = cluster_name
        self.name = name
        self.desired = int(desired)

    def start(self):
        ecs.update_service(
            cluster=self.cluster_name, service=self.name, desiredCount=self.desired
        )
        self.logger.info(f"Service {self.name} started successfully")

    def stop(self):
        ecs.update_service(cluster=self.cluster_name, service=self.name, desiredCount=0)
        self.logger.info(f"Service {self.name} stopped successfully")
