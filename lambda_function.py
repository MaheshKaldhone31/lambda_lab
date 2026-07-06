import json
import os


def handler(event, context):
    name = (event or {}).get("name", "World")
    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": f"Hello, {name}!",
                "environment": os.getenv("ENVIRONMENT", "dev"),
            }
        ),
    }
    return response
