from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_cognito as cognito,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_s3 as s3
)

import aws_cdk as cdk

class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        user_pool = cognito.CfnUserPool(self, "cognitouserpool",
        auto_verified_attributes = [
            'email'
        ],
        username_attributes = [
            'email', 'phone_number'
        ],
        user_pool_name = proj_name+'-user-pool',
        schema = [
            {
                'name': 'Param1',
                'attributeDataType': 'String',
                'mutable': True
            }
        ],
        policies = cognito.CfnUserPool.PoliciesProperty(
            password_policy = cognito.CfnUserPool.PasswordPolicyProperty(
                minimum_length = 10,
                require_lowercase = True,
                require_numbers = True,
                require_symbols = False,
                require_uppercase = True
            )
        )
        )

        user_pool_client = cognito.CfnUserPoolClient(self, 'pool-client',
        user_pool_id = user_pool.ref,
        client_name = env_name+'-app-client'
        )

        identity_pool = cognito.CfnIdentityPool(self, 'identitypool',
        allow_unauthenticated_identities=False,
        cognito_identity_providers =[
            cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                client_id = user_pool_client.ref,
                provider_name = user_pool.attr_provider_name
            )
        ],
        identity_pool_name = proj_name+'-identity-pool'
        )

        ssm.StringParameter(self, 'app-client-id',
        parameter_name= "/"+env_name+'/cognito-app-client-id',
        string_value = user_pool_client.ref
        )

        ssm.StringParameter(self, 'user-pool-id',
        parameter_name= "/"+env_name+'/cognito-user-pool-id',
        string_value = user_pool_client.user_pool_id
        )

        ssm.StringParameter(self, 'identity-pool-id',
        parameter_name= "/"+env_name+'/cognitp-identity-pool-id',
        string_value = identity_pool.ref
        )

