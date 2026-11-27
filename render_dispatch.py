"""Trigger the repository's GitHub Actions monitor from an external scheduler."""
import json
import os
import sys
import urllib.error
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("Missing required environment variable: GITHUB_TOKEN")

url = "https://api.github.com/repos/lukaszsocha1979-boop/crupto-alerts/dispatches"
payload = json.dumps({"event_type": "crypto_alerts_tick"}).encode("utf-8")
request = urllib.request.Request(
    url,
    data=payload,
    method="POST",
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "crypto-alerts-render-scheduler",
    },
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 204:
            sys.exit(f"Unexpected GitHub response: HTTP {response.status}")
        print("GitHub repository_dispatch accepted (HTTP 204).")
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", errors="replace")
    sys.exit(f"GitHub API error HTTP {exc.code}: {body}")
except Exception as exc:
    sys.exit(f"Dispatch failed: {exc}")
