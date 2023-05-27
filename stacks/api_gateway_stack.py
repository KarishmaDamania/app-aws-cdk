from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as apigw,
    aws_ssm as ssm)

import aws_cdk as cdk

class APIStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        account_id = cdk.Aws.ACCOUNT_ID
        region = cdk.Aws.REGION

        api_gateway = apigw.RestApi(self, 'restapi', 
        endpoint_types=[apigw.EndpointType.REGIONAL],
        rest_api_name = proj_name+'-service' )

        api_gateway.root.add_method('ANY')

        ssm.StringParameter(self, 'api-gw',
        parameter_name = "/" + env_name + "/api-gw-url",
        string_value = "https://" + api_gateway.rest_api_id+".execute-api."+region+'.amazonaws.com/')

        ssm.StringParameter(self, 'api-gw-id',
        parameter_name = "/" + env_name + "/api-gw-id",
        string_value = api_gateway.rest_api_id)

