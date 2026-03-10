import json
import os

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # Extract query parameters
    query_params = event.get("queryStringParameters", {})
    name = query_params.get("name", "World")

    # Create response
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Hello, {name}!"
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    return response