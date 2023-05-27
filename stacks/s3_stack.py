from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_s3 as s3
)

import aws_cdk as cdk


class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        account_id = cdk.Aws.ACCOUNT_ID

        lambda_bucket = s3.Bucket(self, 'lambda-bucket',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  bucket_name=account_id+"-"+env_name+"-lambda-deploy-packages",
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  removal_policy=cdk.RemovalPolicy.RETAIN
                                  )

        ssm.StringParameter(self, 'ssm-lambda-bucket',
                            parameter_name="/"+env_name+"/lambda-s3-bucket",
                            string_value=lambda_bucket.bucket_name)


        ## To Store Build Artifacts

        artifacts_bucket = s3.Bucket(self, 'build-artifacts',
            access_control= s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption = s3.BucketEncryption.S3_MANAGED,
            bucket_name = account_id + '-'+env_name+'-build-artifacts',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
        )

        cdk.CfnOutput(self, 's3-build-artifacts-export',
            value = artifacts_bucket.bucket_name,
            export_name='build-artifacts-bucket'
        )

        ## To Store FrontEnd App
        
        frontend_bucket = s3.Bucket(self, 'frontend',
            access_control= s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption = s3.BucketEncryption.S3_MANAGED,
            bucket_name = account_id + '-'+env_name+'-frontend',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
        )

        cdk.CfnOutput(self, 's3-frontend-export',
            value = frontend_bucket.bucket_name,
            export_name='frontend-bucket'
        )
