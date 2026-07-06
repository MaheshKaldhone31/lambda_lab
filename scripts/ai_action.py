#!/usr/bin/env python3

import os
from pathlib import Path
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GEMINI_API_KEY not configured. Skipping AI review.")
    raise SystemExit(0)

client = genai.Client(api_key=api_key)

repo_root = Path.cwd()

files_to_scan = [
    "README.md",
    "Dockerfile",
    "requirements.txt",
    "lambda_function.py",
]

content = ""

for file_name in files_to_scan:
    file_path = repo_root / file_name

    if file_path.exists():
        content += f"\n\n===== {file_name} =====\n"
        content += file_path.read_text(encoding="utf-8")[:5000]

prompt = f"""
You are a Senior DevSecOps Engineer.

Review this repository and provide:

1. Security issues
2. Docker best practices
3. Lambda best practices
4. CI/CD improvements
5. Cost optimization suggestions
6. Overall score out of 10

Repository:

{content}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

report = response.text

with open("ai_summary.txt", "w") as f:
    f.write(report)

print(report)