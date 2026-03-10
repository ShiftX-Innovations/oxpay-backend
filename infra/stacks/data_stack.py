from aws_cdk import (
    Stack, RemovalPolicy, Duration,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct

class DataStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 env_name: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # DB credentials stored in Secrets Manager
        self.db_secret = secretsmanager.Secret(
            self, "DbSecret",
            secret_name=f"oxpay/{env_name}/db-credentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "oxpay_admin"}',
                generate_string_key="password",
                exclude_punctuation=True,
            )
        )

        # Aurora Serverless v2
        self.db = rds.DatabaseCluster(
            self, "OxPayDB",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_15_3
            ),
            cluster_identifier=f"oxpay-{env_name}-db",
            serverless_v2_min_capacity=0.5,
            serverless_v2_max_capacity=2 if env_name == "dev" else 16,
            writer=rds.ClusterInstance.serverless_v2("writer"),
            vpc=vpc,
            credentials=rds.Credentials.from_secret(self.db_secret),
            removal_policy=RemovalPolicy.SNAPSHOT if env_name == "prod"
                           else RemovalPolicy.DESTROY,
        )