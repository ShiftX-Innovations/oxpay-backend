from aws_cdk import (Stack, aws_lambda as _lambda,
    aws_apigateway as apigw, Duration)
from constructs import Construct

class ApiStack(Stack):
    def __init__(self, scope: Construct, id: str,
                 env_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.hello_fn = _lambda.Function(
            self, 'HelloWorldFn',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='handler.handler',
            code=_lambda.Code.from_asset(
                '../backend/functions/hello_world'),
            environment={'ENVIRONMENT': env_name},
            function_name=f'oxpay-hello-world-{env_name}',
            timeout=Duration.seconds(29),
        )

        api = apigw.RestApi(self, 'OxPayApi',
            rest_api_name=f'oxpay-api-{env_name}',
            deploy_options=apigw.StageOptions(stage_name=env_name)
        )

        hello = api.root.add_resource('hello')
        hello.add_method('GET',
            apigw.LambdaIntegration(self.hello_fn))
