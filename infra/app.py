import os
import aws_cdk as cdk
from stacks.network_stack import NetworkStack
from stacks.data_stack import DataStack
from stacks.app_stack import AppStack
from stacks.pipeline_stack import PipelineStack
from stacks.api_stack import ApiStack
from stacks.observability_stack import ObservabilityStack

app = cdk.App()

env_name = app.node.try_get_context('env') or 'dev'

env_config = {
    'dev':     {'account': os.environ['CDK_DEV_ACCOUNT'],     'region': 'ap-southeast-1'},
    'staging': {'account': os.environ['CDK_STAGING_ACCOUNT'], 'region': 'ap-southeast-1'},
    'prod':    {'account': os.environ['CDK_PROD_ACCOUNT'],    'region': 'ap-southeast-1'},
}

aws_env = cdk.Environment(**env_config[env_name])

api = ApiStack(app, f'OxPay-Api-{env_name}',
    env_name=env_name, env=aws_env)

ObservabilityStack(app, f'OxPay-Obs-{env_name}',
    lambda_fn=api.hello_fn, env_name=env_name, env=aws_env)

app.synth()
