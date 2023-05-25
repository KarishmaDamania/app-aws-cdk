import aws_cdk as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_gp_stack import SecurityGpStack

app = cdk.App()

vpc_stack = VPCStack(app, 'VPC')
security_gp_stack = SecurityGpStack(app, "SG", vpc=vpc_stack.vpc)

app.synth()
