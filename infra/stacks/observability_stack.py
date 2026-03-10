from aws_cdk import (Stack, aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns, Duration)
from constructs import Construct

class ObservabilityStack(Stack):
    def __init__(self, scope, id, *,
                 lambda_fn, env_name, **kwargs):
        super().__init__(scope, id, **kwargs)

        topic = sns.Topic(self, 'Alerts',
            topic_name=f'oxpay-alerts-{env_name}')

        cw.Alarm(self, 'ErrorAlarm',
            metric=lambda_fn.metric_errors(
                period=Duration.minutes(1)),
            threshold=1,
            evaluation_periods=1,
            alarm_name=f'oxpay-hello-errors-{env_name}',
        ).add_alarm_action(cw_actions.SnsAction(topic))
