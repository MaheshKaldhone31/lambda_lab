#!/usr/bin/env python3
import os
import sys
from pathlib import Path

try:
    import openai
except Exception:
    print("openai package not installed; exiting.")
    sys.exit(2)


def main() -> int:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set — skipping AI integration.")
        return 0

    openai.api_key = key

    repo_root = Path(__file__).resolve().parents[1]
    readme_path = repo_root / "README.md"
    index_path = repo_root / "index.html"

    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    index = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    prompt = (
        "You are a helpful assistant that analyzes a small Python repository. "
        "Summarize the project in 2-4 sentences and provide 3 concise improvement suggestions.\n\n"
    )
    prompt += "README:\n" + (readme[:4000] or "(no README)") + "\n\n"
    prompt += "Index HTML:\n" + (index[:4000] or "(no index.html)")

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a repository analysis assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.2,
        )
        summary = resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("AI API call failed:", e, file=sys.stderr)
        return 2

    out_path = repo_root / "ai_summary.txt"
    out_path.write_text(summary, encoding="utf-8")
    print("AI summary written to:", out_path)
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
