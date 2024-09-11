# Resource Scheduler

This composition scheduler can be used to schedule compositions with components that can be temporarily stopped, like EC2 instances, RDS instances/clusters and Redshift clusters. It's aimed at:

* Environments that only run during office hours
* Environments that only run on-demand

It has the following high level architecture:

![Architecture](docs/architecture.png)

## Features

### Supported resource types

The following resoure types can be controlled via this scheduler:

* EC2 Auto-Scaling Groups
* ECS Services
* RDS Clusters
* RDS Instances
* Redshift Clusters

RDS only support stopping instances / clusters that are not running in multi-AZ mode.

### Timezone aware

Schedules are timezone aware so there's no need to change them on any DST changes, keeping https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html#daylist-savings-time in mind.

### Control order and wait times

The order in which resources are started- and stopped is controllable. These operations are asynchronous and wait times between activities are configurable.

The stop procedure of a schedule is the reverse of the start procedure.

### Respecting maintenance- and backup windows

When setting up scheduling, the scheduler will check if configured maintenance- and backup windows on RDS instances / clusters and Redshift clusters overlap with the scheduled start- and stop times of a composition. If they don't, an additional schedule will be setup to make sure the cluster is started during the scheduled maintenance- and backup windows.

### Webhooks

Optionally a pair of webhooks can be deployed to trigger starting or stopping an environments based on external events. This allows for on-demand starting or stopping of environments by - for example - a service management ticket, a Slack integration, a custom frontend, a Github workflow, etc.

Webhooks require an API key and can be setup to only allow certain IP addresses.

## Limitations

### Schedule mixing

Most of the supported services allow for their own methods of scheduling, either with or without timezone support. This module can not detect existing schedules so overlapping schedules could contradict each other, resulting in unexpected behaviour.

### RDS snapshot retention

When an RDS instance is stopped, the stopped time does not count towards the retention time of snapshots. Effectively this means that any snapshot will be retained longer than expected, including any associated cost.

This behaviour is described here: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ManagingAutomatedBackups.html

### AWS Backup integration

For AWS Backup to be able to create a backup of an RDS instance, it needs to be running. This module is currently not capable of automatically detecting the schedule of any AWS Backup plans. In such cases you will need to manually align the schedules.

## Setup

To setup this module requires a composition of the resources that need to be managed. Based on that input, a state machine is generated.

Please see the [examples](examples/) folder for code examples of how to implement this module.

## Development

This module uses the integrated Lambda to abstract some of the more complex functionality away. For redistribution purposes, the following dependencies have been vendorized:

* pyawscron 1.0.6: https://pypi.org/project/pyawscron/ - https://github.com/pitchblack408/pyawscron/tree/1.0.6

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5.0 |
| <a name="requirement_archive"></a> [archive](#requirement\_archive) | >= 2.4.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.10.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | >= 2.4.0 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 5.10.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_api_gateway_role"></a> [api\_gateway\_role](#module\_api\_gateway\_role) | github.com/schubergphilis/terraform-aws-mcaf-role | v0.3.3 |
| <a name="module_eventbridge_scheduler_role"></a> [eventbridge\_scheduler\_role](#module\_eventbridge\_scheduler\_role) | github.com/schubergphilis/terraform-aws-mcaf-role | v0.3.3 |
| <a name="module_lambda_role"></a> [lambda\_role](#module\_lambda\_role) | github.com/schubergphilis/terraform-aws-mcaf-role | v0.3.3 |
| <a name="module_scheduler_lambda"></a> [scheduler\_lambda](#module\_scheduler\_lambda) | schubergphilis/mcaf-lambda/aws | ~> 1.1.2 |
| <a name="module_step_functions_role"></a> [step\_functions\_role](#module\_step\_functions\_role) | github.com/schubergphilis/terraform-aws-mcaf-role | v0.3.3 |

## Resources

| Name | Type |
|------|------|
| [aws_api_gateway_api_key.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_api_key) | resource |
| [aws_api_gateway_deployment.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_deployment) | resource |
| [aws_api_gateway_integration.webhook_start_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_integration) | resource |
| [aws_api_gateway_integration.webhook_stop_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_integration) | resource |
| [aws_api_gateway_integration_response.webhook_start_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_integration_response) | resource |
| [aws_api_gateway_integration_response.webhook_stop_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_integration_response) | resource |
| [aws_api_gateway_method.webhook_start_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_method) | resource |
| [aws_api_gateway_method.webhook_stop_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_method) | resource |
| [aws_api_gateway_method_response.webhook_start_composition_200](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_method_response) | resource |
| [aws_api_gateway_method_response.webhook_stop_composition_200](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_method_response) | resource |
| [aws_api_gateway_method_settings.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_method_settings) | resource |
| [aws_api_gateway_model.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_model) | resource |
| [aws_api_gateway_resource.webhook_start_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_resource) | resource |
| [aws_api_gateway_resource.webhook_stop_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_resource) | resource |
| [aws_api_gateway_rest_api.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_rest_api) | resource |
| [aws_api_gateway_rest_api_policy.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_rest_api_policy) | resource |
| [aws_api_gateway_stage.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_stage) | resource |
| [aws_api_gateway_usage_plan.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_usage_plan) | resource |
| [aws_api_gateway_usage_plan_key.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_usage_plan_key) | resource |
| [aws_cloudwatch_log_group.webhooks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_scheduler_schedule.rds_cluster_backup_start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_cluster_backup_stop](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_cluster_maintenance_start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_cluster_maintenance_stop](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_instance_backup_start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_instance_backup_stop](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_instance_maintenance_start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.rds_instance_maintenance_stop](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.redshift_cluster_maintenance_start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.redshift_cluster_maintenance_stop](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.start_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule.stop_composition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_scheduler_schedule_group.scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule_group) | resource |
| [aws_sfn_state_machine.composition_start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.composition_stop](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [archive_file.scheduler_source](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_db_instance.managed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/db_instance) | data source |
| [aws_iam_policy_document.api_gateway_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.eventbridge_scheduler_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambda_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.step_functions_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_lambda_invocation.rds_cluster_backup_windows](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation) | data source |
| [aws_lambda_invocation.rds_cluster_maintenance_windows](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation) | data source |
| [aws_lambda_invocation.rds_instance_backup_windows](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation) | data source |
| [aws_lambda_invocation.rds_instance_maintenance_windows](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation) | data source |
| [aws_lambda_invocation.redshift_cluster_maintenance_windows](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation) | data source |
| [aws_rds_cluster.managed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/rds_cluster) | data source |
| [aws_redshift_cluster.managed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/redshift_cluster) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_composition_name"></a> [composition\_name](#input\_composition\_name) | The name of the controlled composition | `string` | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The ARN of the KMS key to use with the Lambda function | `string` | n/a | yes |
| <a name="input_resource_composition"></a> [resource\_composition](#input\_resource\_composition) | Resource composition | <pre>list(object({<br>    type   = string<br>    params = map(any)<br>  }))</pre> | n/a | yes |
| <a name="input_start_resources_at"></a> [start\_resources\_at](#input\_start\_resources\_at) | Resources start cron expression in selected timezone | `string` | n/a | yes |
| <a name="input_stop_resources_at"></a> [stop\_resources\_at](#input\_stop\_resources\_at) | Resources stop cron expression in selected timezone | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | Mapping of tags | `map(string)` | `{}` | no |
| <a name="input_timezone"></a> [timezone](#input\_timezone) | Timezone to execute schedules in | `string` | `"UTC"` | no |
| <a name="input_webhooks"></a> [webhooks](#input\_webhooks) | Deploy webhooks for external triggers | <pre>object({<br>    deploy       = bool<br>    ip_whitelist = list(string)<br>    private      = optional(bool, false)<br>  })</pre> | <pre>{<br>  "deploy": false,<br>  "ip_whitelist": [],<br>  "private": false<br>}</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_api_gateway_stage_arn"></a> [api\_gateway\_stage\_arn](#output\_api\_gateway\_stage\_arn) | n/a |
| <a name="output_start_composition_webhook_url"></a> [start\_composition\_webhook\_url](#output\_start\_composition\_webhook\_url) | n/a |
| <a name="output_stop_composition_webhook_url"></a> [stop\_composition\_webhook\_url](#output\_stop\_composition\_webhook\_url) | n/a |
| <a name="output_webhook_api_key"></a> [webhook\_api\_key](#output\_webhook\_api\_key) | n/a |
<!-- END_TF_DOCS -->
