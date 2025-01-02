import boto3
from typing import Tuple

from scheduler.resource_controller import ResourceController

EFS_MINIMAL_THROUGHPUT_CAPACITY = 1.0


class EfsFileSystemController(ResourceController):
    client = boto3.client("efs")

    def __init__(
        self,
        id: str,
        provisioned_throughput_in_mibps: str,
    ):
        super().__init__()
        self.id = id
        self.provisioned_throughput_in_mibps = float(
            int(provisioned_throughput_in_mibps)
        )

    def start(self) -> Tuple[bool, str]:
        file_system = self.client.describe_file_systems(FileSystemId=self.id)[
            "FileSystems"
        ][0]
        if file_system["ThroughputMode"] != "provisioned":
            return (
                False,
                f"EFS Filesystem {self.id} is not in provisioned throughput mode",
            )

        self.client.update_file_system(
            FileSystemId=self.id,
            ThroughputMode="provisioned",
            ProvisionedThroughputInMibps=self.provisioned_throughput_in_mibps,
        )

        return (
            True,
            f"Throughput capacity for {self.id} adjusted to {self.provisioned_throughput_in_mibps} MB/s",
        )

    def stop(self) -> Tuple[bool, str]:
        file_system = self.client.describe_file_systems(FileSystemId=self.id)[
            "FileSystems"
        ][0]
        if file_system["ThroughputMode"] != "provisioned":
            return (
                False,
                f"EFS Filesystem {self.id} is not in provisioned throughput mode",
            )

        self.client.update_file_system(
            FileSystemId=self.id,
            ThroughputMode="provisioned",
            ProvisionedThroughputInMibps=EFS_MINIMAL_THROUGHPUT_CAPACITY,
        )

        return (
            True,
            f"Throughput capacity for {self.id} adjusted to {EFS_MINIMAL_THROUGHPUT_CAPACITY} MB/s",
        )
