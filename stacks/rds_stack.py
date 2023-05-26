from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_kms as kms,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_s3 as s3,
    aws_rds as rds,
    aws_secretsmanager as sm,
)

import aws_cdk as cdk

import json


class RDSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, lambdasg: ec2.SecurityGroup, bastionsg: ec2.SecurityGroup, kmskey, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        json_template={'username': 'admin'}
        db_creds = sm.Secret(self, 'db-secret',
            secret_name=env_name+'-rds-secret',
            generate_secret_string=sm.SecretStringGenerator(
                include_space=False,
                exclude_punctuation=True,
                password_length=12,
                generate_string_key='password',
                secret_string_template=json.dumps(json_template)
            )
        )

        print(db_creds)


        db_mysql = rds.DatabaseCluster(self, 'mysql',
            default_database_name=proj_name+env_name,
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
            credentials=rds.Credentials.from_secret(db_creds, "admin"),
            instance_props=rds.InstanceProps(
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
            ),
            instances=1,
            storage_encryption_key = kmskey,
            removal_policy= cdk.RemovalPolicy.DESTROY
        )

        db_mysql.connections.allow_default_port_from(lambdasg, "Access from Lambda Functions")
        db_mysql.connections.allow_default_port_from(bastionsg, "Access from Bastion Host")
        
        ssm.StringParameter(self, 'db-host',
        parameter_name='/'+'env_name'+'/db-host',
        string_value=db_mysql.cluster_endpoint.hostname
        )
