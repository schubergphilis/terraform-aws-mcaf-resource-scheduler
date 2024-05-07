from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validator

import scheduler.schemas as schemas
from scheduler.aws_cron.helper import extend_windows
from scheduler.resource_controllers.ecs_service_controller import EcsServiceController
from scheduler.resource_controllers.auto_scaling_group_controller import (
    AutoscalingGroupController,
)
from scheduler.resource_controllers.rds_cluster_controller import RdsClusterController
from scheduler.resource_controllers.rds_instance_controller import RdsInstanceController
from scheduler.resource_controllers.redshift_cluster_controller import (
    RedshiftClusterController,
)

logger = Logger()


@logger.inject_lambda_context(log_event=True)
@validator(inbound_schema=schemas.INPUT, outbound_schema=schemas.OUTPUT)
def handler(event, _content):
    resource_action = (event["resource_type"], event["action"])
    params = event[f"{event['resource_type']}_params"]

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
            EcsServiceController(**params).start()
        case ("ecs_service", "stop"):
            EcsServiceController(**params).stop()
        case ("auto_scaling_group", "start"):
            AutoscalingGroupController(**params).start()
        case ("auto_scaling_group", "stop"):
            AutoscalingGroupController(**params).stop()
        case ("rds_cluster", "start"):
            RdsClusterController(**params).start()
        case ("rds_cluster", "stop"):
            RdsClusterController(**params).stop()
        case ("rds_instance", "start"):
            RdsInstanceController(**params).start()
        case ("rds_instance", "stop"):
            RdsInstanceController(**params).stop()
        case ("redshift_cluster", "start"):
            RedshiftClusterController(**params).start()
        case ("redshift_cluster", "stop"):
            RedshiftClusterController(**params).stop()
