from aws_cdk import (
    Stack, Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct

class AppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 env_name: str, db_secret_arn: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Shared Lambda environment variables
        common_env = {
            "ENV": env_name,
            "DB_SECRET_ARN": db_secret_arn,
        }

        # Shared IAM role for all Lambdas
        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaVPCAccessExecutionRole"
                )
            ]
        )

        # --- Auth Lambda ---
        auth_fn = _lambda.Function(
            self, "AuthFn",
            function_name=f"oxpay-{env_name}-auth",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/auth"),
            timeout=Duration.seconds(10),
            environment=common_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_MONTH,
        )

        # --- Expense Lambda ---
        # expense_fn = _lambda.Function(
        #     self, "ExpenseFn",
        #     function_name=f"oxpay-{env_name}-expense",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     handler="handler.handler",
        #     code=_lambda.Code.from_asset("lambda/expense"),
        #     timeout=Duration.seconds(15),
        #     environment=common_env,
        #     role=lambda_role,
        # )

        # # --- Payments Lambda ---
        # payments_fn = _lambda.Function(
        #     self, "PaymentsFn",
        #     function_name=f"oxpay-{env_name}-payments",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     handler="handler.handler",
        #     code=_lambda.Code.from_asset("lambda/payments"),
        #     timeout=Duration.seconds(30),
        #     environment=common_env,
        #     role=lambda_role,
        # )

        # # --- API Gateway ---
        # api = apigw.RestApi(
        #     self, "OxPayApi",
        #     rest_api_name=f"oxpay-{env_name}-api",
        #     deploy_options=apigw.StageOptions(
        #         stage_name=env_name,
        #         throttling_rate_limit=500,      # matches NFR: 500 TPS
        #         throttling_burst_limit=1000,
        #     )
        # )

        # # Routes
        # # POST /auth/request-otp
        # auth_res = api.root.add_resource("auth")
        # auth_res.add_resource("request-otp").add_method(
        #     "POST", apigw.LambdaIntegration(auth_fn)
        # )

        # # GET+POST /expense
        # expense_res = api.root.add_resource("expense")
        # expense_res.add_method("GET", apigw.LambdaIntegration(expense_fn))

        # # POST /payments/initiate
        # payments_res = api.root.add_resource("payments")
        # payments_res.add_resource("initiate").add_method(
        #     "POST", apigw.LambdaIntegration(payments_fn)
        # )