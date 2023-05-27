from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_codepipeline as cp,
    aws_codebuild as cb, 
    aws_codepipeline_actions as cp_actions,
    aws_lambda as lb,
    aws_apigateway as apigw,
    aws_ssm as ssm)

import aws_cdk as cdk

class CodePipelineBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, artifactbucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        artifact_bucket= s3.Bucket.from_bucket_name(self, 'artifactbucket', artifactbucket)

        github_token = cdk.SecretValue.secrets_manager(
            env_name+"/github-token", json_field = 'github-token'
        )

        pipeline = cp. Pipeline(self, 'backend-pipeline',
            pipeline_name = env_name+proj_name+'-backend-pipe',
            artifact_bucket=artifactbucket,
            restart_execution_on_update=False
        )

        source_output = cp.Artifact()
