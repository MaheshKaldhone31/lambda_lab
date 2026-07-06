import json
import uuid
import os

TODO_STORE = {}


def get_html_ui():
    """Load and return the HTML UI from index.html."""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return f.read()
    return """
    <html>
    <head><title>Todo App</title></head>
    <body>
        <h1>Todo App</h1>
        <p>HTML UI file not found. API is still available.</p>
        <p>Use API with {"httpMethod":"GET","path":"/todos"}</p>
    </body>
    </html>
    """


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }


def list_todos():
    return build_response(200, {"todos": list(TODO_STORE.values())})


def create_todo(body):
    title = body.get("title")
    if not title or not isinstance(title, str):
        return build_response(400, {"error": "Todo title is required."})

    todo_id = str(uuid.uuid4())
    todo = {"id": todo_id, "title": title, "completed": bool(body.get("completed", False))}
    TODO_STORE[todo_id] = todo
    return build_response(201, todo)


def get_todo(todo_id):
    todo = TODO_STORE.get(todo_id)
    if not todo:
        return build_response(404, {"error": "Todo not found."})
    return build_response(200, todo)


def update_todo(todo_id, body):
    todo = TODO_STORE.get(todo_id)
    if not todo:
        return build_response(404, {"error": "Todo not found."})

    title = body.get("title")
    if title is not None:
        if not isinstance(title, str) or not title:
            return build_response(400, {"error": "Todo title must be a non-empty string."})
        todo["title"] = title

    if "completed" in body:
        todo["completed"] = bool(body["completed"])

    TODO_STORE[todo_id] = todo
    return build_response(200, todo)


def delete_todo(todo_id):
    if todo_id not in TODO_STORE:
        return build_response(404, {"error": "Todo not found."})
    del TODO_STORE[todo_id]
    return build_response(204, {})


def build_html_response(html_content):
    """Return HTML response with proper headers for Function URL."""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": html_content,
    }


def handler(event, context):
    # Handle Lambda Function URL format (convert to API Gateway format)
    if "rawPath" in event and "requestContext" in event:
        # Function URL format
        http_method = event.get("requestContext", {}).get("http", {}).get("method", "GET").upper()
        path = event.get("rawPath", "/todos")
        raw_body = event.get("body")
    else:
        # API Gateway format
        http_method = event.get("httpMethod", "GET").upper()
        path = event.get("path", "/todos")
        raw_body = event.get("body")

    # Handle OPTIONS for CORS preflight
    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": "",
        }

    try:
        body = json.loads(raw_body) if raw_body else {}
    except (TypeError, json.JSONDecodeError):
        response = build_response(400, {"error": "Request body must be valid JSON."})
        response["headers"]["Access-Control-Allow-Origin"] = "*"
        return response

    # Serve HTML UI for root path
    if path in ["/", ""]:
        return build_html_response(get_html_ui())

    if path == "/todos":
        if http_method == "GET":
            return list_todos()
        if http_method == "POST":
            return create_todo(body)
        return build_response(405, {"error": "Method not allowed."})

    if path.startswith("/todos/"):
        todo_id = path.split("/", 2)[-1]
        if http_method == "GET":
            return get_todo(todo_id)
        if http_method in {"PUT", "PATCH"}:
            return update_todo(todo_id, body)
        if http_method == "DELETE":
            return delete_todo(todo_id)
        return build_response(405, {"error": "Method not allowed."})

    return build_response(404, {"error": "Route not found."})
