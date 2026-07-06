import json
import unittest

from lambda_function import TODO_STORE, handler


class TodoAppTests(unittest.TestCase):
    def setUp(self):
        TODO_STORE.clear()
    def test_create_todo(self):
        event = {
            "httpMethod": "POST",
            "path": "/todos",
            "body": json.dumps({"title": "Buy milk"}),
        }

        response = handler(event, None)
        self.assertEqual(response["statusCode"], 201)

        body = json.loads(response["body"])
        self.assertEqual(body["title"], "Buy milk")
        self.assertFalse(body["completed"])
        self.assertIn("id", body)

    def test_list_todos(self):
        create_event = {
            "httpMethod": "POST",
            "path": "/todos",
            "body": json.dumps({"title": "Write tests"}),
        }
        handler(create_event, None)

        list_event = {"httpMethod": "GET", "path": "/todos"}
        response = handler(list_event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertGreaterEqual(len(body["todos"]), 1)
        self.assertEqual(body["todos"][0]["title"], "Write tests")

    def test_update_todo(self):
        create_event = {
            "httpMethod": "POST",
            "path": "/todos",
            "body": json.dumps({"title": "Refactor code"}),
        }
        create_response = handler(create_event, None)
        todo = json.loads(create_response["body"])

        update_event = {
            "httpMethod": "PUT",
            "path": f"/todos/{todo['id']}",
            "body": json.dumps({"completed": True}),
        }
        response = handler(update_event, None)

        self.assertEqual(response["statusCode"], 200)
        updated = json.loads(response["body"])
        self.assertTrue(updated["completed"])

    def test_delete_todo(self):
        create_event = {
            "httpMethod": "POST",
            "path": "/todos",
            "body": json.dumps({"title": "Clean up"}),
        }
        create_response = handler(create_event, None)
        todo = json.loads(create_response["body"])

        delete_event = {
            "httpMethod": "DELETE",
            "path": f"/todos/{todo['id']}",
        }
        response = handler(delete_event, None)
        self.assertEqual(response["statusCode"], 204)


if __name__ == "__main__":
    unittest.main()
