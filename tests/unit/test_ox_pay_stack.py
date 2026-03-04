import aws_cdk as core
import aws_cdk.assertions as assertions

from ox_pay.ox_pay_stack import OxPayStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ox_pay/ox_pay_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OxPayStack(app, "ox-pay")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
