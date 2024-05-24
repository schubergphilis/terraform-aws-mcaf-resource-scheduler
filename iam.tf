data "aws_iam_policy_document" "eventbridge_scheduler_policy" {
  statement {
    effect  = "Allow"
    actions = ["states:StartExecution"]
    resources = [
      aws_sfn_state_machine.composition_start.arn,
      aws_sfn_state_machine.composition_stop.arn
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [module.scheduler_lambda.arn]
  }
}

module "eventbridge_scheduler_role" {
  source = "github.com/schubergphilis/terraform-aws-mcaf-role?ref=v0.3.3"

  name                  = "composition-scheduler-event-bridge-role-${var.composition_name}-${data.aws_region.current.name}"
  create_policy         = true
  postfix               = false
  principal_type        = "Service"
  principal_identifiers = ["scheduler.amazonaws.com"]
  role_policy           = data.aws_iam_policy_document.eventbridge_scheduler_policy.json
  tags                  = var.tags
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:log-group:/aws/lambda/*:*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["kms:ListAliases"]
    resources = ["arn:aws:kms:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:DescribeKey",
      "kms:Encrypt",
      "kms:GenerateDataKey*",
      "kms:ReEncrypt*"
    ]
    resources = [var.kms_key_arn]
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "ecs_service") ? toset(["ecs_service"]) : toset([])

    content {
      effect  = "Allow"
      actions = ["ecs:UpdateService"]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:ecs:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:service/${resource.params["cluster_name"]}/${resource.params["name"]}"
        if resource.type == "ecs_service"
      ]
    }
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "ec2_instance") ? toset(["ec2_instance"]) : toset([])

    content {
      effect = "Allow"
      actions = [
        "ec2:StartInstances",
        "ec2:StopInstances"
      ]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:ec2:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:instance/${resource.params["id"]}"
        if resource.type == "ec2_instance"
      ]
    }
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "auto_scaling_group") ? toset(["auto_scaling_group"]) : toset([])

    content {
      effect  = "Allow"
      actions = ["autoscaling:UpdateAutoScalingGroup"]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:autoscaling:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:autoScalingGroup:*:autoScalingGroupName/${resource.params["name"]}"
        if resource.type == "auto_scaling_group"
      ]
    }
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "auto_scaling_group") ? toset(["auto_scaling_group"]) : toset([])

    content {
      effect  = "Allow"
      actions = ["iam:PassRole"]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:iam::${data.aws_caller_identity.current.id}:role/*"
        if resource.type == "auto_scaling_group"
      ]
      condition {
        test     = "StringEquals"
        variable = "iam:PassedToService"
        values   = ["ec2.amazonaws.com"]
      }
    }
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "redshift_cluster") ? toset(["redshift_cluster"]) : toset([])

    content {
      effect = "Allow"
      actions = [
        "redshift:PauseCluster",
        "redshift:ResumeCluster"
      ]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:redshift:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:cluster:${resource.params["id"]}"
        if resource.type == "redshift_cluster"
      ]
    }
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "rds_cluster") ? toset(["rds_cluster"]) : toset([])

    content {
      effect = "Allow"
      actions = [
        "rds:StartDBCluster",
        "rds:StopDBCluster"
      ]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:rds:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:cluster:${resource.params["id"]}"
        if resource.type == "rds_cluster"
      ]
    }
  }

  dynamic "statement" {
    for_each = contains(local.resource_types_in_composition, "rds_instance") ? toset(["rds_instance"]) : toset([])

    content {
      effect = "Allow"
      actions = [
        "rds:StartDBInstance",
        "rds:StopDBInstance"
      ]
      resources = [
        for resource in var.resource_composition :
        "arn:aws:rds:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:db:${resource.params["id"]}"
        if resource.type == "rds_instance"
      ]
    }
  }
}

module "lambda_role" {
  source = "github.com/schubergphilis/terraform-aws-mcaf-role?ref=v0.3.3"

  name                  = "composition-scheduler-lambda-role-${var.composition_name}-${data.aws_region.current.name}"
  create_policy         = true
  postfix               = false
  principal_type        = "Service"
  principal_identifiers = ["lambda.amazonaws.com"]
  role_policy           = data.aws_iam_policy_document.lambda_policy.json
  tags                  = var.tags
}

data "aws_iam_policy_document" "step_functions_policy" {
  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [module.scheduler_lambda.arn]
  }
}

module "step_functions_role" {
  source = "github.com/schubergphilis/terraform-aws-mcaf-role?ref=v0.3.3"

  name                  = "composition-scheduler-step-functions-role-${var.composition_name}-${data.aws_region.current.name}"
  create_policy         = true
  postfix               = false
  principal_type        = "Service"
  principal_identifiers = ["states.amazonaws.com"]
  role_policy           = data.aws_iam_policy_document.step_functions_policy.json
  tags                  = var.tags
}

data "aws_iam_policy_document" "api_gateway_policy" {
  statement {
    effect = "Allow"
    actions = [
      "states:StartExecution",
      "states:StopExecution"
    ]
    resources = [
      aws_sfn_state_machine.composition_start.arn,
      aws_sfn_state_machine.composition_stop.arn,
      "${aws_sfn_state_machine.composition_start.arn}:*",
      "${aws_sfn_state_machine.composition_stop.arn}:*",
    ]
  }
}

module "api_gateway_role" {
  count  = var.webhooks.deploy ? 1 : 0
  source = "github.com/schubergphilis/terraform-aws-mcaf-role?ref=v0.3.3"

  name                  = "composition-scheduler-api-gateway-role-${var.composition_name}-${data.aws_region.current.name}"
  create_policy         = true
  postfix               = false
  principal_type        = "Service"
  principal_identifiers = ["apigateway.amazonaws.com"]
  role_policy           = data.aws_iam_policy_document.api_gateway_policy.json
  tags                  = var.tags
}
