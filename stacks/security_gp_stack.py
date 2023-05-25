from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ssm as ssm
)


class SecurityGpStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        lambda_sg = ec2.SecurityGroup(self,
                                      "lambdasg",
                                      security_group_name='lambda-sg',
                                      vpc=vpc,
                                      description="SG for Lambda Functions",
                                      allow_all_outbound=True
                                      )

        self.bastion_sg = ec2.SecurityGroup(self,
                                            "bastionsg",
                                            security_group_name='bastion-sg',
                                            vpc=vpc,
                                            description="SG for Bastion Host",
                                            allow_all_outbound=True
                                            )
        self.bastion_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH Access")

        lambda_role = iam.Role(self, 'lambdarole',
                               assumed_by=iam.ServicePrincipal(
                                   service="lambda.amazonaws.com"),
                               role_name='lambda-role',
                               managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                   managed_policy_name="service-role/AWSLambdaBasicExecutionRole")
                               ]
                               )

        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=["s3:*", "rds:*"],
                resources=["*"]
            )
        )

        # SSM Parameters

        ssm.StringParameter(self, "lambdasg-param",
                            parameter_name="/"+env_name+"/lambda-sg",
                            string_value=lambda_sg.security_group_id
                            )

        ssm.StringParameter(self, "lambdarole-param",
                            parameter_name="/"+env_name+"/lambda-role-arn",
                            string_value=lambda_role.role_arn)

        ssm.StringParameter(self, "lambdarole-param-name",
                            parameter_name="/"+env_name+"/lambda-role-name",
                            string_value=lambda_role.role_name)
