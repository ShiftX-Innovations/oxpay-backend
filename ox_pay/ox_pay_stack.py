# from aws_cdk import (
#     # Duration,
#     Stack,
#     # aws_sqs as sqs,
# )
# from constructs import Construct

# class OxPayStack(Stack):

#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         # The code that defines your stack goes here

#         # example resource
#         # queue = sqs.Queue(
#         #     self, "OxPayQueue",
#         #     visibility_timeout=Duration.seconds(300),
#         # )

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct

class OxPayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # --- Lambda Function: Auth ---
        auth_lambda = _lambda.Function(
            self, "AuthHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",      # file.function_name
            code=_lambda.Code.from_asset("lambda/auth"),
            timeout=Duration.seconds(10),
        )

        # --- API Gateway ---
        api = apigw.RestApi(
            self, "OxPayApi",
            rest_api_name="OxPay API",
            description="OxPay Backend API",
        )

        # Route: POST /auth/request-otp
        auth_resource = api.root.add_resource("auth")
        otp_resource = auth_resource.add_resource("request-otp")
        otp_resource.add_method(
            "POST",
            apigw.LambdaIntegration(auth_lambda)
        )