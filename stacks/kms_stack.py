from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_kms as kms
)


class KMSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        self.kms_rds = kms.Key(self, 'rdskey',
                               description="{}-key-rds ".format(proj_name),
                               enable_key_rotation=True
                               )

        self.kms_rds.add_alias(
            alias_name='alias/{}-key-rds'.format(proj_name)
        )
