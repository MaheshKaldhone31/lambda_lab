# Python Lambda sample app

This repository contains a minimal Python application for AWS Lambda that can be deployed from GitHub Actions.

## Files

- `lambda_function.py` — Lambda handler entry point
- `tests/test_lambda_function.py` — basic unit tests
- `Dockerfile` — container image definition for Lambda
- `.github/workflows/deploy.yml` — GitHub Actions workflow for zip-based deployment
- `.github/workflows/deploy-docker.yml` — GitHub Actions workflow for Docker-based Lambda deployment

## Local testing

Run the tests locally:

```bash
python -m unittest discover -s tests -v
```

## GitHub Actions deployment

Set these repository settings before enabling the workflow:

- Repository variable: `AWS_REGION`
- Repository variable: `LAMBDA_FUNCTION_NAME`
- Repository variable: `ECR_REPOSITORY_NAME` (required for the Docker workflow)
- Repository secret: `AWS_ROLE_TO_ASSUME`

The Docker workflow uses GitHub OIDC to assume the AWS role, build the Lambda container image, push it to Amazon ECR, and deploy it to Lambda.

If you want to add AI-related validation later, you can place those steps in the `Future AI integration readiness` section of the workflow.

## Lambda invocation example

```bash
aws lambda invoke \
  --function-name YOUR_FUNCTION_NAME \
  --payload '{"name":"GitHub Actions"}' \
  response.json
```
