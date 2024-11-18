import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController

fsx = boto3.client("fsx")


class FsxWindowsFileSystemController(ResourceController):
    def __init__(
        self,
        id: str,
        start_throughput_capacity: int,
        stop_throughput_capacity: int,
    ):
        super().__init__()
        self.id = id
        self.start_throughput_capacity = int(start_throughput_capacity)
        self.stop_throughput_capacity = int(stop_throughput_capacity)

    def start(self) -> Tuple[bool, str]:
        fsx.update_file_system(
            FileSystemId=self.id,
            WindowsConfiguration={"ThroughputCapacity": self.start_throughput_capacity},
        )
        return (
            True,
            f"Throughput capacity for {self.id} started adjusted to {self.start_throughput_capacity} MB/s",
        )

    def stop(self) -> Tuple[bool, str]:
        fsx.update_file_system(
            FileSystemId=self.id,
            WindowsConfiguration={"ThroughputCapacity": self.stop_throughput_capacity},
        )
        return (
            True,
            f"Throughput capacity for {self.id} started adjusted to {self.stop_throughput_capacity} MB/s",
        )
