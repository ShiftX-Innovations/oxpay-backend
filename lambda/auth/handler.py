import json

def handler(event, context):
    """
    POST /auth/request-otp
    Handles OTP request for email login (Section 5.1)
    """
    body = json.loads(event.get("body", "{}"))
    email = body.get("email")

    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Email is required"})
        }

    # TODO: generate 6-digit OTP, store in DB with 5-min expiry, send email
    print(f"OTP requested for: {email}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "OTP sent", "email": email})
    }