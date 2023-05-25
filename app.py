import aws_cdk as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_gp_stack import SecurityGpStack
from stacks.bastion_host import BastionStack


app = cdk.App()

vpc_stack = VPCStack(app, 'VPC')
security_gp_stack = SecurityGpStack(app, "SG", vpc=vpc_stack.vpc)
bastion_stack = BastionStack(
    app, "Bastion", vpc=vpc_stack.vpc, sg=security_gp_stack.bastion_sg)


app.synth()
