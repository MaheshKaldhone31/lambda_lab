import json
import unittest

from lambda_function import handler


class LambdaHandlerTests(unittest.TestCase):
    def test_handler_returns_greeting(self):
        response = handler({"name": "Alice"}, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["message"], "Hello, Alice!")

    def test_handler_uses_default_name(self):
        response = handler({}, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["message"], "Hello, World!")


if __name__ == "__main__":
    unittest.main()
