#!/usr/bin/env python3

import os
from pathlib import Path
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("OPENAI_API_KEY not configured. Skipping AI review.")
    exit(0)

client = OpenAI(api_key=API_KEY)

repo_root = Path.cwd()

files_to_scan = [
    "README.md",
    "Dockerfile",
    "requirements.txt",
    "lambda_function.py",
    ".github/workflows/deploy-docker.yml",
]

content = ""

for file_name in files_to_scan:
    file_path = repo_root / file_name

    if file_path.exists():
        try:
            content += f"\n\n===== {file_name} =====\n"
            content += file_path.read_text(encoding="utf-8")[:5000]
        except Exception as e:
            print(f"Could not read {file_name}: {e}")

prompt = f"""
You are a senior DevSecOps engineer.

Review this repository and provide:

1. Security vulnerabilities
2. CI/CD issues
3. Docker best practices
4. AWS Lambda best practices
5. GitHub Actions improvements
6. Code quality recommendations

Repository content:

{content}
"""

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert DevSecOps reviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    report = response.choices[0].message.content

    with open("ai-security-report.md", "w") as f:
        f.write(report)

    print("\n===== AI SECURITY REPORT =====\n")
    print(report)

except Exception as e:
    print(f"AI review failed: {e}")
    exit(1)