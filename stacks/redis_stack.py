from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_elasticache as redis,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_s3 as s3
)

import aws_cdk as cdk

class RedisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, redissg, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        proj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        subnets = [subnet.subnet_id for subnet in vpc.private_subnets]

        subnet_group = redis.CfnSubnetGroup(self, 'redis-subnet-group',
        subnet_ids = subnets,
        description="Subnet Group For Redis"
        )

        redis_cluster = redis.CfnCacheCluster(self, 'redis',
        cache_node_type='cache.t2.small',
        engine='redis',
        num_cache_nodes=1,
        cluster_name=proj_name+'-redis'+env_name,
        cache_subnet_group_name=subnet_group.ref,
        vpc_security_group_ids=[redissg],
        auto_minor_version_upgrade=True)

        redis_cluster.add_depends_on(subnet_group)

        ssm.StringParameter(self, 'redis-endpoint',
        parameter_name='/'+env_name+'/redis-endpoint',
        string_value=redis_cluster.attr_redis_endpoint_address)

        ssm.StringParameter(self, 'redis-port',
        parameter_name='/'+env_name+'/redis-port',
        string_value=redis_cluster.attr_redis_endpoint_port)