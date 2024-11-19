import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController

MINIMAL_THROUGHPUT_CAPACITY = 32

fsx = boto3.client("fsx")


class FsxWindowsFileSystemController(ResourceController):
    def __init__(
        self,
        id: str,
        throughput_capacity: str,
    ):
        super().__init__()
        self.id = id
        self.throughput_capacity = int(throughput_capacity)

    def start(self) -> Tuple[bool, str]:
        fsx.update_file_system(
            FileSystemId=self.id,
            WindowsConfiguration={"ThroughputCapacity": self.throughput_capacity},
        )
        return (
            True,
            f"Throughput capacity for {self.id} started adjusted to {self.throughput_capacity} MB/s",
        )

    def stop(self) -> Tuple[bool, str]:
        fsx.update_file_system(
            FileSystemId=self.id,
            WindowsConfiguration={"ThroughputCapacity": MINIMAL_THROUGHPUT_CAPACITY},
        )
        return (
            True,
            f"Throughput capacity for {self.id} started adjusted to {MINIMAL_THROUGHPUT_CAPACITY} MB/s",
        )
