# Webhooks

This example starts resources at 09:00 AM on weekdays and shuts them down again at 06:00 PM.

When starting the resources it follows these steps:

1. Giving the RDS instance with id `application-cluster-1` a start command.
1. Waits 10 minutes for the RDS instance to become available.
1. Update the ECS service named `application-service-1` on ECS cluster `application-cluster-1` and put the number of desired tasks in the service to 2.

These steps are executed in reverse when stopping the instances.

The RDS instance will also be started 15 minutes before its configured maintenance- and backup window. It will be stopped 15 minutes after its configured maintenance- and backup window. The ECS service is unaffected during these windows.

Additional to the scheduled start/stop of the mentioned resources, an API Gateway is deployed that provides endpoints for webhooks that can be used for automation from external resources. Think starting/stopping a bunch of resources from a ticketing system or via ChatOps.
