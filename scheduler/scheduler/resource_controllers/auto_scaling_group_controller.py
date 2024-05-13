import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController

autoscaling = boto3.client("autoscaling")


class AutoscalingGroupController(ResourceController):
    def __init__(self, name: str, min: str, max: str, desired: str):
        super().__init__()
        self.name = name
        self.min = int(min)
        self.max = int(max)
        self.desired = int(desired)

    def start(self) -> Tuple[bool, str]:
        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=self.name,
            MinSize=self.min,
            MaxSize=self.max,
            DesiredCapacity=self.desired,
        )
        return (True, f"Auto-Scaling Group {self.name} started successfully")

    def stop(self) -> Tuple[bool, str]:
        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=self.name, MinSize=0, MaxSize=0, DesiredCapacity=0
        )
        return (True, f"Auto-Scaling Group {self.name} stopped successfully")
