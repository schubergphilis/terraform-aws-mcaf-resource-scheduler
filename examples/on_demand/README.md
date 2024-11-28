# On-Demand

This example never starts resources on a schedule, but will always attempt to shut them down at 06:00 PM. There are no webhooks configured in this example, meaning the state machine that starts resources will have to be triggered in some other way.

When starting the resources it follows these steps:

1. Giving the RDS instance with id `application-cluster-1` a start command.
1. Giving the FSx Windows File System a throughput of 256 MB/s.
1. Waits 10 minutes for the RDS instance to become available.
1. Update the ECS service named `application-service-1` on ECS cluster `application-cluster-1` and put the number of desired tasks in the service to 2.

These steps are executed in reverse when stopping the instances.

The RDS instance will also be started 15 minutes before its configured maintenance- and backup window. It will be stopped 15 minutes after its configured maintenance- and backup window. The ECS service is unaffected during these windows.
