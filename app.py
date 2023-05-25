import aws_cdk as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_gp_stack import SecurityGpStack
from stacks.bastion_host_stack import BastionStack
from stacks.kms_stack import KMSStack
from stacks.s3_stack import S3Stack

app = cdk.App()

vpc_stack = VPCStack(app, 'VPC')

security_gp_stack = SecurityGpStack(app, "SG", vpc=vpc_stack.vpc)

bastion_stack = BastionStack(
    app, "Bastion", vpc=vpc_stack.vpc, sg=security_gp_stack.bastion_sg)

kms_stack = KMSStack(app, "KMS")

s3_stack = S3Stack(app, "S3")

app.synth()
