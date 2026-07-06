#!/usr/bin/env python3

import os
import sys
import time
from pathlib import Path

from google import genai


def read_file(path):
    try:
        return Path(path).read_text(encoding="utf-8")[:10000]
    except Exception:
        return ""


def get_repository_content():
    files_to_scan = [
        "README.md",
        "lambda_function.py",
        "Dockerfile",
        "requirements.txt",
        ".github/workflows/deploy-docker.yml",
    ]

    content = ""

    for file in files_to_scan:
        if Path(file).exists():
            content += f"\n\n===== {file} =====\n"
            content += read_file(file)

    return content


def generate_ai_review(prompt):
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    retries = 3

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                time.sleep(10)
            else:
                raise


def main():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY not configured.")
        sys.exit(0)

    repo_content = get_repository_content()

    prompt = f"""
You are a senior DevSecOps engineer.

Analyze this repository.

Provide:

1. Security findings
2. Vulnerabilities
3. Docker best practices
4. Lambda best practices
5. GitHub Actions improvements
6. Infrastructure recommendations

Output in markdown format.

Repository:

{repo_content}
"""

    try:
        result = generate_ai_review(prompt)

        report_file = "ai_security_review.md"

        with open(report_file, "w") as f:
            f.write(result)

        print("\n=== AI SECURITY REVIEW ===\n")
        print(result)

        print(f"\nReport written to {report_file}")

    except Exception as e:
        print(f"AI review failed: {e}")

        with open("ai_security_review.md", "w") as f:
            f.write(
                f"# AI Review Failed\n\nError:\n\n{str(e)}"
            )

        sys.exit(0)


if __name__ == "__main__":
    main()