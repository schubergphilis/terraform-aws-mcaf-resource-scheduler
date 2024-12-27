from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validator
from typing import Dict

import scheduler.schemas as schemas
from scheduler.cron_helper import extend_windows
from scheduler.resource_controllers.auto_scaling_group_controller import (
    AutoScalingGroupController,
)
from scheduler.resource_controllers.ec2_instance_controller import Ec2InstanceController
from scheduler.resource_controllers.ecs_service_controller import EcsServiceController
from scheduler.resource_controllers.efs_file_system_controller import (
    EfsFileSystemController,
)
from scheduler.resource_controllers.fsx_windows_file_system_controller import (
    FsxWindowsFileSystemController,
)
from scheduler.resource_controllers.rds_cluster_controller import RdsClusterController
from scheduler.resource_controllers.rds_instance_controller import RdsInstanceController
from scheduler.resource_controllers.redshift_cluster_controller import (
    RedshiftClusterController,
)

logger = Logger()


@logger.inject_lambda_context(log_event=True)
@validator(inbound_schema=schemas.INPUT, outbound_schema=schemas.OUTPUT)
def handler(event, _context) -> Dict:
    resource_action = (event["resource_type"], event["action"])
    params = event[f"{event['resource_type']}_params"]

    success, msg = (False, "Unknown resource action")
    match resource_action:
        case ("cron_helper", "extend_windows"):
            extended_windows = extend_windows(**params)
            return {
                "start": extended_windows[0],
                "stop": extended_windows[1],
                "skip_start": extended_windows[2],
                "skip_stop": extended_windows[3],
            }
        case ("ecs_service", "start"):
            success, msg = EcsServiceController(**params).start()
        case ("ecs_service", "stop"):
            success, msg = EcsServiceController(**params).stop()
        case ("auto_scaling_group", "start"):
            success, msg = AutoScalingGroupController(**params).start()
        case ("auto_scaling_group", "stop"):
            success, msg = AutoScalingGroupController(**params).stop()
        case ("ec2_instance", "start"):
            success, msg = Ec2InstanceController(**params).start()
        case ("ec2_instance", "stop"):
            success, msg = Ec2InstanceController(**params).stop()
        case ("rds_cluster", "start"):
            success, msg = RdsClusterController(**params).start()
        case ("rds_cluster", "stop"):
            success, msg = RdsClusterController(**params).stop()
        case ("rds_instance", "start"):
            success, msg = RdsInstanceController(**params).start()
        case ("rds_instance", "stop"):
            success, msg = RdsInstanceController(**params).stop()
        case ("redshift_cluster", "start"):
            success, msg = RedshiftClusterController(**params).start()
        case ("redshift_cluster", "stop"):
            success, msg = RedshiftClusterController(**params).stop()
        case ("fsx_windows_file_system", "start"):
            success, msg = FsxWindowsFileSystemController(**params).start()
        case ("fsx_windows_file_system", "stop"):
            success, msg = FsxWindowsFileSystemController(**params).stop()
        case ("efs_file_system", "start"):
            success, msg = EfsFileSystemController(**params).start()
        case ("efs_file_system", "stop"):
            success, msg = EfsFileSystemController(**params).stop()

    if success:
        logger.info(msg)
    else:
        logger.warning(msg)

    return {"success": success, "message": msg}
