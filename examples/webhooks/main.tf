module "scheduler" {
  source = "../.."

  composition_name = "sample-composition-app-1"

  kms_key_arn = "arn:aws:kms:eu-west-1:000000000000:key/4216b078-39ad-42fa-8a9d-f1c2d68f90b3"

  resource_composition = [
    {
      "type" : "rds_instance",
      "params" : {
        "id" : "application-cluster-1"
      }
    },
    {
      "type" : "efs_file_system",
      "params" : {
        "id" : "efs-file-system-1",
        "provisioned_throughput_in_mibps" : 128
      }
    },
    {
      "type" : "wait",
      "params" : {
        "seconds" : 600
      }
    },
    {
      "type" : "ecs_service",
      "params" : {
        "cluster_name" : "application-cluster-1",
        "name" : "application-service-1",
        "desired" : 2
      }
    }
  ]

  webhooks = {
    deploy       = true
    ip_whitelist = ["10.1.2.0/24"]
    private      = true
  }

  start_resources_at = "0 9 ? * MON-FRI *"
  stop_resources_at  = "0 18 ? * MON-FRI *"
  timezone           = "Europe/Amsterdam"
}
