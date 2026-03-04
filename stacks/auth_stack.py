from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    aws_codebuild as codebuild,
    aws_secretsmanager as sm,
)
from constructs import Construct

class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Source artifact (your GitHub code)
        source_output = codepipeline.Artifact("SourceOutput")
        build_output = codepipeline.Artifact("BuildOutput")

        # CodeBuild - Build + Synth
        build_project = codebuild.PipelineProject(
            self, "BuildProject",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
            )
        )

        pipeline = codepipeline.Pipeline(
            self, "OxPayPipeline",
            pipeline_name="oxpay-pipeline",
            stages=[

                # Stage 1: Pull from GitHub
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        actions.CodeStarConnectionsSourceAction(
                            action_name="GitHub_Source",
                            owner="YOUR_GITHUB_USERNAME",   # ← change this
                            repo="oxpay-backend",           # ← change this
                            branch="main",
                            output=source_output,
                            connection_arn="YOUR_CODESTAR_CONNECTION_ARN",  # ← step 5
                        )
                    ]
                ),

                # Stage 2: Build + CDK Synth
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        actions.CodeBuildAction(
                            action_name="Build_and_Synth",
                            project=build_project,
                            input=source_output,
                            outputs=[build_output],
                        )
                    ]
                ),

                # Stage 3: Deploy Dev (automatic)
                codepipeline.StageProps(
                    stage_name="Deploy_Dev",
                    actions=[
                        actions.CloudFormationCreateUpdateStackAction(
                            action_name="Deploy_Dev",
                            stack_name="OxPay-App-dev",
                            template_path=build_output.at_path(
                                "cdk.out/OxPay-App-dev.template.json"
                            ),
                            admin_permissions=True,
                        )
                    ]
                ),

                # Stage 4: Manual Approval before Staging
                codepipeline.StageProps(
                    stage_name="Approve_Staging",
                    actions=[
                        actions.ManualApprovalAction(
                            action_name="Dev_Lead_Approval",
                            notify_emails=["devlead@oxpay.com"],  # ← change
                        )
                    ]
                ),

                # Stage 5: Deploy Staging (automatic after approval)
                codepipeline.StageProps(
                    stage_name="Deploy_Staging",
                    actions=[
                        actions.CloudFormationCreateUpdateStackAction(
                            action_name="Deploy_Staging",
                            stack_name="OxPay-App-staging",
                            template_path=build_output.at_path(
                                "cdk.out/OxPay-App-staging.template.json"
                            ),
                            admin_permissions=True,
                        )
                    ]
                ),

                # Stage 6: Manual Approval before Prod (client sign-off)
                codepipeline.StageProps(
                    stage_name="Approve_Prod",
                    actions=[
                        actions.ManualApprovalAction(
                            action_name="Client_UAT_Approval",
                            notify_emails=["client@oxpay.com"],  # ← change
                        )
                    ]
                ),

                # Stage 7: Deploy Prod
                codepipeline.StageProps(
                    stage_name="Deploy_Prod",
                    actions=[
                        actions.CloudFormationCreateUpdateStackAction(
                            action_name="Deploy_Prod",
                            stack_name="OxPay-App-prod",
                            template_path=build_output.at_path(
                                "cdk.out/OxPay-App-prod.template.json"
                            ),
                            admin_permissions=True,
                        )
                    ]
                ),
            ]
        )