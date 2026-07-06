# Python Lambda todo app

This repository contains a minimal Python AWS Lambda todo application that can be run locally and deployed with GitHub Actions.

## Files

- `lambda_function.py` — Lambda handler entry point for a simple todo API
- `tests/test_lambda_function.py` — unit tests for the todo API
- `Dockerfile` — container image definition for Lambda
- `.github/workflows/deploy.yml` — GitHub Actions workflow for zip-based deployment
- `.github/workflows/deploy-docker.yml` — GitHub Actions workflow for Docker-based Lambda deployment

## Todo API

The Lambda handler supports the following routes when invoked as an API Gateway proxy:

- `GET /todos` — list all todos
- `POST /todos` — create a todo with JSON body `{ "title": "..." }`
- `GET /todos/{id}` — retrieve a single todo
- `PUT /todos/{id}` — update a todo
- `DELETE /todos/{id}` — delete a todo

## Local testing

Run the tests locally:

```bash
python -m unittest discover -s tests -v
```

## GitHub Actions: AI integration

An optional GitHub Actions workflow (`.github/workflows/ai-integration.yml`) can run an AI analysis step that summarizes the repository and writes `ai_summary.txt`.

To enable it:

- Add a repository secret named `OPENAI_API_KEY` with your OpenAI API key.
- The workflow runs on pushes to `main` and on pull requests; the AI step only runs when the secret is present.

The workflow calls `scripts/ai_action.py` which uses the `openai` Python package. Install the dependency via `pip install -r requirements.txt`.

## Lambda invocation example

```bash
aws lambda invoke \
  --function-name YOUR_FUNCTION_NAME \
  --payload '{"httpMethod":"POST","path":"/todos","body":"{\"title\":\"Buy milk\"}"}' \
  response.json
```

The function returns JSON responses and uses a simple in-memory todo store while the Lambda runtime is warm.
