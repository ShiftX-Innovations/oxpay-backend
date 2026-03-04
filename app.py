# #!/usr/bin/env python3
# import os

# import aws_cdk as cdk

# from ox_pay.ox_pay_stack import OxPayStack


# app = cdk.App()
# OxPayStack(app, "OxPayStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.

#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.

#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */

#     #env=cdk.Environment(account='123456789012', region='us-east-1'),

#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )

# app.synth()

import aws_cdk as cdk
from stacks.network_stack import NetworkStack
from stacks.data_stack import DataStack
from stacks.app_stack import AppStack
from stacks.pipeline_stack import PipelineStack

app = cdk.App()

# Deploy stacks for each environment
for env_name in ["dev", "staging", "prod"]:
    network = NetworkStack(app, f"OxPay-Network-{env_name}", env_name=env_name)

    data = DataStack(app, f"OxPay-Data-{env_name}",
                     env_name=env_name,
                     vpc=network.vpc)

    AppStack(app, f"OxPay-App-{env_name}",
             env_name=env_name,
             db_secret_arn=data.db_secret.secret_arn)

# Pipeline stack (deployed once)
PipelineStack(app, "OxPay-Pipeline")

app.synth()